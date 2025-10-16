
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      env-type   = "${var.environment_name}"
      created-by = "Terraform"
      # fisma-id   = "393764" TODO: add when this is determined
      sys-name   = "csfeer"
      acronym    = "csfeer"
    }
  }
}

terraform {
  required_version = ">= 1.11.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.49.0"

    }

    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "~> 1.25.0"
    }
  }

  backend "s3" {}
}
