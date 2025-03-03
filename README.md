# tfblocks
❗️ Very experimental - use at your own risk!

A utility that generates Terraform `import` or `removed` blocks for AWS resources by parsing your Terraform state. This can be particularly useful for safely migrating sets of resources between different Terraform states.

## Quick Start

The easiest way to use `tfblocks` is with [uv](https://github.com/astral-sh/uv):

**Run without installing:**
```bash
terraform show -json | uvx git+https://github.com/stekern/tfblocks tfblocks import
```

**Install as a tool:**
```bash
uv tool install git+https://github.com/stekern/tfblocks
terraform show -json | tfblocks import
```

## Safety Note

This tool is **non-destructive** and has no direct impact on your infrastructure:
- It only reads Terraform state JSON from stdin and outputs to stdout
- No API calls are made to AWS or any other provider
- No files are modified unless you redirect the output 
- Always verify the generated blocks with `terraform plan` before applying
- Never run `terraform apply` without carefully reviewing the plan first

## What & Why
While working with Terraform state recently, I noticed something: even though `import` and `removed` blocks are super helpful additions to Terraform, figuring out the correct import ID format for each resource is still pretty tedious. Ideally, this would be exposed directly on Terraform resources for us to retrieve programmatically. But alas, the formats are only documented in the Terraform AWS provider docs through informal and semi-structured examples. With 1000+ AWS resources, that's a lot of documentation to parse manually. So I wondered - could we automate this?


So Claude Haiku 3.5 and I got to work. I fed it the AWS provider docs and had it create Python classes that could generate the right(ish) import ID for each resource based on the documentation examples. After some quick cleanup and manual testing, here's the result.


Fair warning: there are very likely bugs lurking in the ID formats. This utility can give you a better starting point than writing everything from scratch, but make sure to carefully check your `terraform plan` after using any generated imports. Incorrect import IDs may result in either error messages or unexpected diffs in the plan output - always review thoroughly before applying.

## Usage
```
tfblocks [command] [options] [addresses...]
```

### Commands
- `import` - Generate import blocks
- `remove` - Generate removed blocks
- `list` - Output resource addresses only

### Options
- `--files`, `-f` - Filter resources to those found in specified Terraform files
- `--no-color` - Disable colored output
- `--destroy` - Set destroy = true in removed blocks (only with `remove` command)

## Examples
### Generate import blocks for all AWS resources
```
terraform show -json | tfblocks import
```

### Generate import block for a specific AWS resource
```
terraform show -json | tfblocks import "aws_s3_bucket.this"
```

### Generate import blocks for AWS resources in a specific module
```
terraform show -json | tfblocks import "module.my_module"
```

### Generate import blocks for AWS resources in multiple modules
```
terraform show -json | tfblocks import "module.my_module" "module.my_new_module"
```

### Generate import blocks for AWS resources in specific files
```
terraform show -json | tfblocks import -f "main.tf"
```

### Generate removed blocks for all AWS resources
```
terraform show -json | tfblocks remove
```

### Generate removed blocks with destroy=true
```
terraform show -json | tfblocks remove --destroy
```

### List all resource addresses
```
terraform show -json | tfblocks list
```
