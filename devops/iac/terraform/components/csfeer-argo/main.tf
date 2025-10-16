
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      env-type   = "${var.environment_name}"
      created-by = "Terraform"
      sys-name = "CSFEER"
      acronym  = "csfeer"
    }
  }
}

ephemeral "aws_eks_cluster_auth" "this" {
  name = data.aws_eks_cluster.csfeer_eks_cluster.name
}

terraform {
  required_version = ">= 1.11.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"

    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.24.0"
    }

  }

  backend "s3" {}
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.csfeer_eks_cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.csfeer_eks_cluster.certificate_authority[0].data)
  token                  = ephemeral.aws_eks_cluster_auth.this.token
}
