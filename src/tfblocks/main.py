import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

import tfblocks.aws_resources as aws_resources


def get_aws_resource_import_id_generators() -> Dict[str, type]:
    """Get all classes from aws_resources module with snake_case keys"""
    return {
        re.sub(r"(?<!^)(?=[A-Z])", "_", cls).lower(): getattr(aws_resources, cls)
        for cls in dir(aws_resources)
        if isinstance(getattr(aws_resources, cls), type)
    }


def extract_addresses_from_content(content: str) -> List[str]:
    """Extract resource and module addresses from Terraform content."""
    addresses = []

    # Match resource blocks
    resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"'
    resources = re.finditer(resource_pattern, content)
    for match in resources:
        addresses.append(f"{match.group(1)}.{match.group(2)}")

    # Match module blocks
    module_pattern = r'module\s+"([^"]+)"'
    modules = re.finditer(module_pattern, content)
    for match in modules:
        addresses.append(f"module.{match.group(1)}")

    return addresses


def extract_addresses_from_file(file_path: str) -> List[str]:
    """Extract resource and module addresses from a Terraform file."""
    addresses = []

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file_path, "r") as f:
            content = f.read()

        addresses = extract_addresses_from_content(content)

    except Exception as e:
        print(f"Warning: Could not process file {file_path}: {str(e)}", file=sys.stderr)

    if not addresses:
        print(
            f"Warning: No resources or modules found in file {file_path}",
            file=sys.stderr,
        )

    return addresses


def is_resource_match(
    resource_addr: str, filter_addrs: List[str] = [], file_addrs: List[str] = []
) -> bool:
    """Check if resource address matches the filter conditions.

    If both filter_addrs and file_addrs are provided, the resource must match both (intersection).
    If only one type of filter is provided, the resource must match that filter.
    If no filters are provided, all resources match.

    Supports wildcards (*) in filter addresses for pattern matching.
    """

    def extract_resource_type_and_name(addr: str) -> tuple:
        """Extract resource type and name from a full address."""
        # For resources in modules, we need to extract just the final resource part
        parts = addr.split(".")
        if len(parts) >= 2:
            # Last two parts should be resource_type.resource_name
            if not parts[-2].startswith("module"):
                return parts[-2], parts[-1]
        return None, None

    def matches_address_list(addr: str, addr_list: List[str]) -> bool:
        for filter_addr in addr_list:
            # Check for wildcard pattern matching
            if "*" in filter_addr:
                # Convert wildcard pattern to regex pattern
                # Escape special regex chars except '*'
                pattern = "^" + re.escape(filter_addr).replace("\\*", ".*") + "$"
                if re.match(pattern, addr):
                    return True

            # Exact match
            if addr == filter_addr:
                return True

            # Extract the base address without the index/key for both resources and modules
            base_addr_pattern = r'^(.+?)(\[\d+\]|\[".+?"\]|\[\'.+?\'\])(.*)$'
            base_addr_match = re.match(base_addr_pattern, addr)

            if base_addr_match:
                # Get the base address and any remaining part after the index
                base_addr = base_addr_match.group(1)

                # Check if the base address matches the filter
                if base_addr == filter_addr:
                    return True

                # Handle nested modules with indices
                if filter_addr.startswith("module.") and base_addr.startswith(
                    f"{filter_addr}."
                ):
                    return True

            # Standard module prefix match (for non-indexed modules)
            if filter_addr.startswith("module.") and addr.startswith(f"{filter_addr}."):
                return True

            # For file addresses, we need to check if the resource type and name match
            # even if the full address is different due to modules
            resource_type, resource_name = extract_resource_type_and_name(addr)
            filter_type, filter_name = extract_resource_type_and_name(filter_addr)

            if resource_type and resource_name and filter_type and filter_name:
                if resource_type == filter_type and resource_name == filter_name:
                    return True

        return False

    # If no filters provided, include everything
    if not filter_addrs and not file_addrs:
        return True

    # If only address filters provided
    if filter_addrs and not file_addrs:
        return matches_address_list(resource_addr, filter_addrs)

    # If only file filters provided
    if file_addrs and not filter_addrs:
        return matches_address_list(resource_addr, file_addrs)

    # If both filters provided, must match both (intersection)
    return matches_address_list(resource_addr, filter_addrs) and matches_address_list(
        resource_addr, file_addrs
    )


def filter_resources(
    state: Dict[str, Any], addresses: List[str] = [], files: List[str] = []
) -> List[Dict[str, Any]]:
    """Extract matching resources from Terraform state."""
    # Extract addresses from files if provided
    file_addresses = []
    if files:
        for file_path in files:
            extracted = extract_addresses_from_file(file_path)
            file_addresses.extend(extracted)

        if not file_addresses:
            print(
                "Warning: No resources or modules found in any of the specified files.",
                file=sys.stderr,
            )
            print("No resources will be included in the output.", file=sys.stderr)
            return []

    resources = []
    modules_to_process = [state["values"]["root_module"]]

    while modules_to_process:
        module = modules_to_process.pop()

        # Add child modules to processing queue
        modules_to_process.extend(module.get("child_modules", []))

        # Process resources in current module
        for resource in module.get("resources", []):
            if resource.get("mode") == "managed" and is_resource_match(
                resource["address"], addresses, file_addresses
            ):
                resources.append(resource)

    if not resources and (addresses or files):
        print(
            "Warning: No resources found matching the specified filters.",
            file=sys.stderr,
        )

    return resources


def generate_import_block(
    resource: Dict[str, Any],
    schema_classes: Dict[str, type],
    supported_providers_only: bool = False,
) -> str | None:
    """Generate Terraform import block for a resource."""
    provider_name = resource["type"].split("_")[0] if "_" in resource["type"] else ""

    if provider_name == "aws":
        # For AWS resources, we have import ID generators
        matching_class = schema_classes.get(resource["type"])
        documentation = f"https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/{resource['type'].replace('aws_', '')}#import"
        import_id = f'"" # TODO: {documentation}'

        if matching_class:
            try:
                instance = matching_class(resource["address"], resource["values"])
                if instance.import_id is not None:
                    import_id = f'"{instance.import_id}"'
            except Exception:
                pass
    elif not supported_providers_only:
        # For providers we don't have import ID generators for
        # we create a block with a link to the resource documentation
        resource_type = resource["type"]

        # Use provider_name field when available to get the right documentation URL
        if resource.get("provider_name", "").startswith("registry.terraform.io/"):
            parts = resource["provider_name"].split("/")
            if len(parts) >= 3:
                org = parts[1]
                provider = parts[2]
                # Best-effort attempt at linking to the right place
                docs_url = f"https://registry.terraform.io/providers/{org}/{provider}/latest/docs/resources/{resource_type.removeprefix(f'{provider_name}_')}#import"
                import_id = f'"" # TODO: {docs_url}'
            else:
                import_id = '"" # TODO'
        else:
            # Fallback to generic message if provider is not on the Terraform registry
            import_id = '"" # TODO'
    else:
        # For unsupported providers when restricting to supported providers only
        return None  # Skip this resource

    return f"""import {{
  to = {resource["address"]}
  id = {import_id}
}}"""


def generate_removed_block(resource_addr: str, destroy: bool = False) -> str:
    """Generate Terraform removed block for a resource or module."""
    destroy_line = "\n    destroy = true" if destroy else "\n    destroy = false"

    # Strip instance keys from the resource address for the 'from' attribute
    # This handles both count and for_each indices
    base_addr = re.sub(r'(\[\d+\]|\[".+?"\]|\[\'.+?\'\])', "", resource_addr)

    return f"""removed {{
  from = {base_addr}
  lifecycle {{{destroy_line}
  }}
}}"""


def generate_blocks_for_command(
    resources: List[Dict[str, Any]],
    command: str,
    destroy: bool = False,
    supported_providers_only: bool = False,
) -> List[str]:
    """Generate Terraform code blocks based on command."""
    blocks = []

    if command == "remove":
        # For removed blocks, deduplicate based on the base address
        base_addresses = set()

        for resource in resources:
            # Strip instance keys to get the base address
            base_addr = re.sub(
                r'(\[\d+\]|\[".+?"\]|\[\'.+?\'\])', "", resource["address"]
            )

            # Only add a removed block if we haven't seen this base address before
            if base_addr not in base_addresses:
                base_addresses.add(base_addr)
                blocks.append(generate_removed_block(resource["address"], destroy))
    elif command == "import":
        # For import blocks, we need the full resource data
        schema_classes = get_aws_resource_import_id_generators()
        blocks = [
            block
            for block in [
                generate_import_block(r, schema_classes, supported_providers_only)
                for r in resources
            ]
            if block is not None
        ]
    else:
        raise ValueError(f"Invalid command '{command}'")
    return blocks


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Terraform blocks utility for generating and managing Terraform blocks",
        epilog="Example usage: terraform show -json | tfblocks import [resource_addresses]",
    )

    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Command to execute", required=True
    )

    # Common filter arguments function
    def add_filter_args(cmd_parser: argparse.ArgumentParser):
        cmd_parser.add_argument(
            "addresses",
            nargs="*",
            help="Optional module or resource addresses to filter by",
        )
        cmd_parser.add_argument(
            "--files", "-f", nargs="+", help="Optional Terraform files to filter by"
        )

    import_parser = subparsers.add_parser("import", help="Generate import blocks")
    add_filter_args(import_parser)
    import_parser.add_argument(
        "--supported-providers-only",
        action="store_true",
        help="Only generate import IDs for supported providers (currently only AWS)",
    )

    remove_parser = subparsers.add_parser("remove", help="Generate removed blocks")
    add_filter_args(remove_parser)
    remove_parser.add_argument(
        "--destroy",
        action="store_true",
        help="Set destroy = true in removed blocks (default is false)",
    )

    list_parser = subparsers.add_parser(
        "list", help="List addresses delimited by newlines"
    )
    add_filter_args(list_parser)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    state = json.load(sys.stdin)
    if state.get("format_version") != "1.0":
        print(
            "Error: Unsupported state file format version. Expected version '1.0'.",
            file=sys.stderr,
        )
        sys.exit(1)
    resources = filter_resources(state, args.addresses, args.files)

    if args.command == "list":
        for resource in resources:
            print(resource["address"])
        return

    blocks = generate_blocks_for_command(
        resources,
        args.command,
        getattr(args, "destroy", False),
        getattr(args, "supported_providers_only", False),
    )

    if args.no_color:
        print("\n\n".join(blocks))
    else:
        if args.command == "import":
            print("\033[92m" + "\n\n".join(blocks) + "\033[0m")
        elif args.command == "remove":
            print("\033[91m" + "\n\n".join(blocks) + "\033[0m")
        else:
            print("\033[92m" + "\n\n".join(blocks) + "\033[0m")


if __name__ == "__main__":
    main()
