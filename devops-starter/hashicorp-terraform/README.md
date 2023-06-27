## Terraform getting started

A tool for managing infrastracture with configuration files.

---

### Setup

(_Note: Each configuration should be on its own folder._)

- Install Tertaform

  https://developer.hashicorp.com/terraform/downloads

- Initialize Terraform to install necessary dependencies

  `terraform init`

- Check execution plan

  `terraform plan`

- Create the resource

  `terraform apply`

- Stop the container

  `terraform destroy`

- Format the configuration file

  `terraform fmt`

- Validate

  `terraform validate`

### Variable definitions

- Using config file named: `variables.tf`

- Using command line: `terraform apply -var "container_name=replacedcontainername"`

### Defining specific outputs after applying the configuration.

1. Create the `outputs.tf` file

2. Run `terraform apply` to see the defined outputs

3. Or run `terraform output`
