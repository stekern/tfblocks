import argparse
import glob
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import tfblocks.aws_resources as aws_resources


def get_aws_resource_import_id_generators() -> Dict[str, type]:
    """Get all classes from aws_resources module with snake_case keys.

    Converts PascalCase class names to snake_case for resource type matching.
    """
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


def extract_address_segment(resource_address: str) -> Optional[str]:
    """Extract resource type and name from a full resource address.

    Handles resources both with and without module prefixes.
    """
    # For resources in modules, we need to extract just the final resource part
    parts = resource_address.split(".")
    # Ensure we have at least type.name, potentially prefixed by modules
    if len(parts) >= 2 and not parts[-2].startswith("module"):
        return ".".join([parts[-2], parts[-1]])
    # Handle direct resource without module prefix
    elif len(parts) == 2 and not parts[0].startswith("module"):
        return ".".join([parts[0], parts[1]])
    return None


def matches_resource_address_filter(
    resource_address: str, resource_address_filter: str
) -> bool:
    """Check if a resource address matches a given resource address filter.

    Handles wildcard patterns, exact matches, indexed resources, and module-prefixed resources.
    """
    if "*" in resource_address_filter:
        # Convert wildcard pattern to regex pattern
        # Escape special regex chars except '*'
        pattern = "^" + re.escape(resource_address_filter).replace("\\*", ".*") + "$"
        if re.match(pattern, resource_address):
            return True

    # Exact match
    if resource_address == resource_address_filter:
        return True

    # Extract the base address without the index or key for both resources and modules
    base_address_pattern = r'^(.+?)(\[\d+\]|\[".+?"\]|\[\'.+?\'\])(.*)$'
    base_address_match = re.match(base_address_pattern, resource_address)
    if base_address_match:
        base_address = base_address_match.group(1)
        # Check if the base address matches the filter
        if base_address == resource_address_filter:
            return True

        # Handle nested modules with indices: filter 'module.a', address 'module.a[0].resource.b'
        if resource_address_filter.startswith("module.") and base_address.startswith(
            f"{resource_address_filter}."
        ):
            return True

    # Standard module prefix match (for non-indexed modules): filter 'module.a', address 'module.a.resource.b'
    if resource_address_filter.startswith("module.") and resource_address.startswith(
        f"{resource_address_filter}."
    ):
        return True

    # Check if resource type and name match, even if module paths differ
    res_type_name = extract_address_segment(resource_address)
    filter_type_name = extract_address_segment(resource_address_filter)

    if res_type_name and filter_type_name and res_type_name == filter_type_name:
        return True

    return False


def matches_filters(
    resource_address: str,
    filter_resource_addresses: List[str] = [],
    resource_addresses_by_file: Dict[str, List[str]] = {},
) -> Tuple[bool, Optional[str]]:
    """Check if resource address matches the filter conditions and return matching filename if applicable.

    - If only filter addresses are provided, checks against that list.
    - If only file addresses are provided, checks against the addresses within those files.
    - If both are provided, the resource must match both (intersection).
    - If neither is provided, the resource matches by default.

    Returns a tuple: (matches: bool, matching_filename: Optional[str]).
    The matching_filename is returned when a match occurred due to file filtering.

    Supports wildcards (*) in filter addresses for pattern matching.
    """

    matches_address_filter = any(
        matches_resource_address_filter(resource_address, filter_resource_address)
        for filter_resource_address in filter_resource_addresses
    )

    matching_filename = next(
        (
            filename
            for filename, resource_addresses_in_file in resource_addresses_by_file.items()
            if any(
                matches_resource_address_filter(
                    resource_address, resource_address_in_file
                )
                for resource_address_in_file in resource_addresses_in_file
            )
        ),
        None,
    )
    matches_files_filter = matching_filename is not None

    # Determine final match based on which filters were active
    # If both filters are present, both must match (intersection)
    # If only one filter type is present, only that one needs to match
    # If no filters are present, it matches
    match = (matches_address_filter or not filter_resource_addresses) and (
        matches_files_filter or not resource_addresses_by_file
    )

    return (match, matching_filename)


def filter_resources(
    state: Dict[str, Any], addresses: List[str] = [], files: List[str] = []
) -> Dict[Optional[str], List[Dict[str, Any]]]:
    """Extract matching resources from Terraform state, grouped by matching file if applicable.

    Traverses the state's module hierarchy to find resources matching the specified filters.
    Returns a dictionary where keys are filenames (from `files`) or None (if no file filtering
    or match wasn't file-specific), and values are lists of matching resources.
    """
    resource_addresses_by_file: Optional[Dict[str, List[str]]] = {}
    for file_path in files:
        extracted = extract_addresses_from_file(file_path)
        if extracted:
            resource_addresses_by_file[file_path] = extracted

    if files and not len(resource_addresses_by_file):
        print(
            "Warning: No resources found in any of the specified files",
            file=sys.stderr,
        )

    # Dictionary to hold results, keyed by filename or None
    grouped_resources: Dict[Optional[str], List[Dict[str, Any]]] = {}
    modules_to_process = [state["values"]["root_module"]]

    while modules_to_process:
        module = modules_to_process.pop()

        # Add child modules to processing queue
        modules_to_process.extend(module.get("child_modules", []))

        # Process resources in current module
        for resource in module.get("resources", []):
            if resource.get("mode") == "managed":
                matches, matching_file = matches_filters(
                    resource["address"], addresses, resource_addresses_by_file
                )
                if matches:
                    # Group by filename if file filtering caused the match, otherwise group under None
                    key = matching_file if resource_addresses_by_file else None
                    if key not in grouped_resources:
                        grouped_resources[key] = []
                    grouped_resources[key].append(resource)

    if not grouped_resources and (addresses or files):
        print(
            "Warning: No resources found matching the specified filters.",
            file=sys.stderr,
        )

    return grouped_resources


def generate_import_block(
    resource: Dict[str, Any],
    schema_classes: Dict[str, type],
    supported_providers_only: bool = False,
) -> Optional[str]:
    """Generate Terraform import block for a resource.

    Uses import ID generators for AWS resources and creates placeholder blocks with
    documentation links for other providers. Returns None for unsupported providers
    when supported_providers_only is True.
    """
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

        import_id = '"" # TODO'
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
        # For unsupported providers when restricting to supported providers only
        return None  # Skip this resource

    return f"""import {{
  to = {resource["address"]}
  id = {import_id}
}}"""


def generate_removed_block(resource_address: str, destroy: bool = False) -> str:
    """Generate Terraform removed block for a resource or module.

    Strips instance keys from the address and includes appropriate lifecycle configuration.
    """
    destroy_line = "\n    destroy = true" if destroy else "\n    destroy = false"

    # Strip instance keys from the resource address for the 'from' attribute
    # This handles both count and for_each indices
    base_address = re.sub(r'(\[\d+\]|\[".+?"\]|\[\'.+?\'\])', "", resource_address)

    return f"""removed {{
  from = {base_address}
  lifecycle {{{destroy_line}
  }}
}}"""


def generate_moved_block(resource_address: str) -> str:
    """Generate Terraform moved block for a resource.

    Creates a moved block for the resource with the original address as both 'from' and 'to',
    with a TODO marker for the user to update the destination address.
    """
    return f"""moved {{
  from = {resource_address}
  to   = {resource_address} # TODO
}}"""


def generate_blocks_for_command(
    resources: List[Dict[str, Any]],
    command: str,
    destroy: bool = False,
    supported_providers_only: bool = False,
) -> List[str]:
    """Generate Terraform code blocks based on the specified command.

    Handles import, remove, and move commands, applying appropriate formatting
    and options for each block type.
    """
    blocks: list[str] = []

    if command == "remove":
        # For removed blocks, deduplicate based on the base address
        base_addresses = set()

        for resource in resources:
            # Strip instance keys to get the base address
            base_address = re.sub(
                r'(\[\d+\]|\[".+?"\]|\[\'.+?\'\])', "", resource["address"]
            )

            # Only add a removed block if we haven't seen this base address before
            if base_address not in base_addresses:
                base_addresses.add(base_address)
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
    elif command == "move":
        blocks = [generate_moved_block(resource["address"]) for resource in resources]
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
        help="Only generate import blocks for providers that have import ID generators (currently only AWS)",
    )

    remove_parser = subparsers.add_parser("remove", help="Generate removed blocks")
    add_filter_args(remove_parser)
    remove_parser.add_argument(
        "--destroy",
        action="store_true",
        help="Set destroy = true in removed blocks (default is false)",
    )

    move_parser = subparsers.add_parser("move", help="Generate moved blocks")
    add_filter_args(move_parser)

    list_parser = subparsers.add_parser(
        "list", help="List addresses of resources delimited by newlines"
    )
    add_filter_args(list_parser)

    args = parser.parse_args()
    return args


def expand_file_patterns(patterns: List[str] = []) -> List[str]:
    """Expand glob patterns and return a sorted list of unique existing files.

    Handles both glob patterns and direct file paths, warning if no files match.
    """
    if not patterns:
        return []

    expanded_files = set()
    for pattern in patterns:
        # Try to glob the pattern first
        matched_files = [f for f in glob.glob(pattern) if os.path.isfile(f)]

        # If no matches but pattern is a file, add it directly
        if not matched_files and os.path.isfile(pattern):
            expanded_files.add(pattern)
        else:
            expanded_files.update(matched_files)

    if not expanded_files:
        print(
            "Warning: No existing files matched the patterns provided via --files.",
            file=sys.stderr,
        )

    return sorted(expanded_files)


def main():
    args = parse_args()
    try:
        state = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from stdin: {e}", file=sys.stderr)
        sys.exit(1)

    if state.get("format_version") != "1.0":
        print(
            "Error: Unsupported state file format version. Expected version '1.0'.",
            file=sys.stderr,
        )
        sys.exit(1)

    expanded_files = expand_file_patterns(args.files)
    grouped_resources = filter_resources(state, args.addresses, expanded_files)

    if args.command == "list":
        # For list, print all matching addresses regardless of grouping
        all_resources = [
            res for res_list in grouped_resources.values() for res in res_list
        ]
        # Sort for consistent output
        all_resources.sort(key=lambda r: r["address"])
        for resource in all_resources:
            print(resource["address"])
        return

    output_parts = []
    # Sort filenames for consistent output order, placing None (no file filter) first
    sorted_filenames = sorted(grouped_resources.keys(), key=lambda x: (x is None, x))

    for filename in sorted_filenames:
        resources_for_group = grouped_resources[filename]
        if not resources_for_group:
            continue
        resources_for_group = sorted(resources_for_group, key=lambda r: r["address"])

        blocks = generate_blocks_for_command(
            resources_for_group,
            args.command,
            getattr(args, "destroy", False),
            getattr(args, "supported_providers_only", False),
        )

        if not blocks:
            continue

        group_output = []
        # Add file comment if grouping by file
        if filename is not None:
            group_output.append(f"{'#' * 80}\n# Source file: {filename}\n{'#' * 80}")

        group_output.append("\n\n".join(blocks))
        # Join with double newline if there was a comment, otherwise single
        joiner = "\n\n" if filename is not None else "\n"
        output_parts.append(joiner.join(group_output))

    final_output = "\n\n".join(output_parts)

    command_colors = {"import": "\033[92m", "remove": "\033[91m", "move": "\033[33m"}

    if args.no_color:
        print(final_output)
    elif color := command_colors.get(args.command, None):
        print(f"{color}{final_output}\033[0m")


if __name__ == "__main__":
    main()
