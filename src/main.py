#!/usr/bin/env python3
import argparse
import json
import re
import sys
from typing import Any, Dict, List

import aws_resources


def get_aws_resource_import_id_generators() -> Dict[str, type]:
    """Get all classes from aws_resources module with snake_case keys"""
    return {
        re.sub(r"(?<!^)(?=[A-Z])", "_", cls).lower(): getattr(aws_resources, cls)
        for cls in dir(aws_resources)
        if isinstance(getattr(aws_resources, cls), type)
    }


def extract_resource_addresses_from_file(file_path: str) -> List[str]:
    """Extract resource and module addresses from a Terraform file."""
    addresses = []
    try:
        with open(file_path, "r") as f:
            content = f.read()

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

    except Exception as e:
        print(f"Warning: Could not process file {file_path}: {str(e)}", file=sys.stderr)

    return addresses


def is_resource_match(
    resource_addr: str, filter_addrs: List[str], file_addrs: List[str]
) -> bool:
    """Check if resource address matches the filter conditions.

    If both filter_addrs and file_addrs are provided, the resource must match both (intersection).
    If only one type of filter is provided, the resource must match that filter.
    If no filters are provided, all resources match.
    """

    def matches_address_list(addr: str, addr_list: List[str]) -> bool:
        for filter_addr in addr_list:
            if addr == filter_addr:
                return True
            if filter_addr.startswith("module.") and addr.startswith(f"{filter_addr}."):
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
    resources = []

    # Extract addresses from files if provided
    file_addresses = []
    if files:
        for file_path in files:
            file_addresses.extend(extract_resource_addresses_from_file(file_path))

    def process_module(module: Dict[str, Any]):
        # Handle resources in current module
        for resource in module.get("resources", []):
            if (
                resource.get("type", "").startswith("aws_")
                and resource.get("mode") == "managed"
                and is_resource_match(resource["address"], addresses, file_addresses)
            ):
                resources.append(resource)

        # Recursively process child modules
        for child in module.get("child_modules", []):
            process_module(child)

    # Process entire root module (including nested modules)
    process_module(state["values"]["root_module"])
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

    return f"""removed {{
  from = {resource_addr}
  lifecycle {{{destroy_line}
  }}
}}"""


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate Terraform import or removed blocks for AWS resources based on Terraform state"
    )
    parser.add_argument(
        "addresses",
        nargs="*",
        help="Optional module or resource addresses to filter by",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        help="Optional Terraform files to filter by",
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )
    parser.add_argument(
        "--removed",
        action="store_true",
        help="Generate removed blocks instead of import blocks",
    )
    parser.add_argument(
        "--destroy",
        action="store_true",
        help="Set destroy = true in removed blocks (default is false)",
    )
    return parser.parse_args()


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

    if args.removed:
        # For removed blocks, we just need the resource addresses
        blocks = [generate_removed_block(r["address"], args.destroy) for r in resources]
    else:
        # For import blocks, we need the full resource data
        schema_classes = get_aws_resource_import_id_generators()
        blocks = [generate_import_block(r, schema_classes) for r in resources]

    if args.no_color:
        print("\n\n".join(blocks))
    else:
        print("\033[92m" + "\n\n".join(blocks) + "\033[0m")


if __name__ == "__main__":
    main()
