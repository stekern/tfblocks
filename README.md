# terraform-aws-import-generator
❗️ Very experimental - use at your own risk!

A utility that parses your Terraform state and generates `import` blocks for AWS resources.

## What & Why
While working with Terraform state recently, I noticed something: even though `import` and `removed` blocks are super helpful additions to Terraform, figuring out the correct import ID format for each resource is still pretty tedious. Ideally, this would be exposed directly on Terraform resources for us to retrieve programmatically. But alas, the formats are only documented in the Terraform AWS provider docs through informal and semi-structured examples. With 1000+ AWS resources, that's a lot of documentation to parse manually. So I wondered - could we automate this?


So Claude Haiku 3.5 and I got to work. I fed it the AWS provider docs and had it create Python classes that could generate the right(ish) import ID for each resource based on the documentation examples. After some quick cleanup and manual testing, here's the result.


Fair warning: there are very likely bugs lurking in the ID formats. This utility can give you a better starting point than writing everything from scratch, but make sure to carefully check your `terraform plan` after using any generated imports.

## Examples
### Generate import blocks for all AWS resources
`terraform show -json | python src/main.py`

### Generate import block for a specific AWS resource
`terraform show -json | python src/main.py aws_s3_bucket.this`

### Generate import blocks for AWS resources in a specific module
`terraform show -json | python src/main.py "module.my_module"`

### Generate import blocks for AWS resources in multiple modules
`terraform show -json | python src/main.py "module.my_module" "module.my_new_module"`
