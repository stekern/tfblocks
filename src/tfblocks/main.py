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


def file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    return os.path.exists(file_path)

def extract_resource_addresses_from_content(content: str) -> List[str]:
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

def extract_resource_addresses_from_file(file_path: str) -> List[str]:
    """Extract resource and module addresses from a Terraform file."""
    addresses = []
    
    # First check if file exists
    if not file_exists(file_path):
        print(f"Error: File {file_path} does not exist", file=sys.stderr)
        sys.exit(1)
        
    try:
        with open(file_path, "r") as f:
            content = f.read()
            
        addresses = extract_resource_addresses_from_content(content)

    except Exception as e:
        print(f"Warning: Could not process file {file_path}: {str(e)}", file=sys.stderr)

    if not addresses:
        print(f"Warning: No resources or modules found in file {file_path}", file=sys.stderr)
        
    return addresses


def is_resource_match(
    resource_addr: str, filter_addrs: List[str], file_addrs: List[str]
) -> bool:
    """Check if resource address matches the filter conditions.

    If both filter_addrs and file_addrs are provided, the resource must match both (intersection).
    If only one type of filter is provided, the resource must match that filter.
    If no filters are provided, all resources match.
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
            # Exact match
            if addr == filter_addr:
                return True

            # Extract the base address without the index/key for both resources and modules
            base_addr_pattern = r'^(.+?)(\[\d+\]|\[".+?"\]|\[\'.+?\'\])(.*)$'
            base_addr_match = re.match(base_addr_pattern, addr)

            if base_addr_match:
                # Get the base address and any remaining part after the index
                base_addr = base_addr_match.group(1)
                remaining = base_addr_match.group(3)

                # Check if the base address matches the filter
                if base_addr == filter_addr:
                    return True

                # Handle nested modules with indices
                if filter_addr.startswith("module.") and base_addr.startswith(f"{filter_addr}."):
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
    """Extract matching AWS managed resources from state."""
    # Extract addresses from files if provided
    file_addresses = []
    if files:
        for file_path in files:
            extracted = extract_resource_addresses_from_file(file_path)
            file_addresses.extend(extracted)
        
        if not file_addresses:
            print("Warning: No resources or modules found in any of the specified files.", file=sys.stderr)
            print("No resources will be included in the output.", file=sys.stderr)
            return []

    resources = []
    modules_to_process = [state["values"]["root_module"]]

    # Iterative approach instead of recursion
    while modules_to_process:
        module = modules_to_process.pop()

        # Add child modules to processing queue
        modules_to_process.extend(module.get("child_modules", []))

        # Process resources in current module
        for resource in module.get("resources", []):
            if (
                resource.get("type", "").startswith("aws_")
                and resource.get("mode") == "managed"
                and is_resource_match(resource["address"], addresses, file_addresses)
            ):
                resources.append(resource)

    if not resources and (addresses or files):
        print("Warning: No resources found matching the specified filters.", file=sys.stderr)

    return resources


def generate_import_block(
    resource: Dict[str, Any], schema_classes: Dict[str, type]
) -> str:
    """Generate import block for a resource."""
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

    return f"""import {{
  to = {resource["address"]}
  id = {import_id}
}}"""


def generate_removed_block(resource_addr: str, destroy: bool = False) -> str:
    """Generate removed block for a resource or module."""
    destroy_line = "\n    destroy = true" if destroy else "\n    destroy = false"

    # Strip instance keys from the resource address for the 'from' attribute
    # This handles both count and for_each indices
    base_addr = re.sub(r'(\[\d+\]|\[".+?"\]|\[\'.+?\'\])', "", resource_addr)

    return f"""removed {{
  from = {base_addr}
  lifecycle {{{destroy_line}
  }}
}}"""


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Terraform blocks utility for generating and managing Terraform blocks",
        epilog="Example usage: terraform show -json | tfblocks import [resource_addresses]"
    )

    # Global options
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )

    # Create subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute", required=True)

    # Common filter arguments function
    def add_filter_args(cmd_parser):
        cmd_parser.add_argument(
            "addresses",
            nargs="*",
            help="Optional module or resource addresses to filter by",
        )
        cmd_parser.add_argument(
            "--files", "-f", nargs="+", help="Optional Terraform files to filter by"
        )

    # Import command
    import_parser = subparsers.add_parser("import", help="Generate import blocks")
    add_filter_args(import_parser)

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Generate removed blocks")
    add_filter_args(remove_parser)
    remove_parser.add_argument(
        "--destroy",
        action="store_true",
        help="Set destroy = true in removed blocks (default is false)",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List resource addresses")
    add_filter_args(list_parser)

    # No default command - require explicit command
    args = parser.parse_args()
    return args


def generate_blocks_for_command(
    resources: List[Dict[str, Any]], command: str, destroy: bool = False
) -> List[str]:
    """Generate appropriate blocks based on command."""
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
    else:  # import command
        # For import blocks, we need the full resource data
        schema_classes = get_aws_resource_import_id_generators()
        blocks = [generate_import_block(r, schema_classes) for r in resources]

    return blocks


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
        # Just output the addresses
        for resource in resources:
            print(resource["address"])
        return

    # Generate blocks based on command
    blocks = generate_blocks_for_command(
        resources, args.command, getattr(args, "destroy", False)
    )

    # Output results
    if args.no_color:
        print("\n\n".join(blocks))
    else:
        print("\033[92m" + "\n\n".join(blocks) + "\033[0m")


if __name__ == "__main__":
    main()
