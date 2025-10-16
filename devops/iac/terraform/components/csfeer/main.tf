provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      env-type   = "${var.environment_name}"
      created-by = "Terraform"
      sys-name   = "CSFEER"
      acronym    = "CSFEER"
    }
  }
}

terraform {
  required_version = ">= 1.11.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.94.0"

    }
  }

  backend "s3" {}
}
