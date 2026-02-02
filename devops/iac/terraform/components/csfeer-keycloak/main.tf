terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }

  backend "s3" {
    key = "dev/csfeer-keycloak.tfstate"
  }
}

provider "aws" {
  region = var.aws_region
}
