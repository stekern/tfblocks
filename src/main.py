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


def is_resource_match(resource_addr: str, filter_addrs: List[str]) -> bool:
    """Check if resource address matches any of the filter addresses."""
    if not filter_addrs:
        return True
    for addr in filter_addrs:
        if resource_addr == addr:
            return True
        if addr.startswith("module.") and resource_addr.startswith(f"{addr}."):
            return True
    return False


def filter_resources(
    state: Dict[str, Any], addresses: List[str]
) -> List[Dict[str, Any]]:
    """Extract matching AWS managed resources from state."""
    resources = []

    def process_module(module: Dict[str, Any]):
        # Handle resources in current module
        for resource in module.get("resources", []):
            if (
                resource.get("type", "").startswith("aws_")
                and resource.get("mode") == "managed"
                and is_resource_match(resource["address"], addresses)
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
    import_id = '""  # TODO'

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


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate Terraform import blocks for AWS resources based on Terraform state"
    )
    parser.add_argument(
        "addresses",
        nargs="*",
        help="Optional module or resource addresses to filter by",
    )
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    state = json.load(sys.stdin)
    schema_classes = get_aws_resource_import_id_generators()

    resources = filter_resources(state, args.addresses)
    imports = [generate_import_block(r, schema_classes) for r in resources]

    if args.no_color:
        print("\n\n".join(imports))
    else:
        print("\033[92m" + "\n\n".join(imports) + "\033[0m")


if __name__ == "__main__":
    main()
