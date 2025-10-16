data "aws_caller_identity" "current" {}

data "terraform_remote_state" "csfeer" {
  backend   = "s3"
  workspace = "csfeer"

  config = {
    bucket = "${var.tf_state_bucket}"
    key    = "${var.environment_name}/state.tfstate"
    region = var.aws_region
  }
}
data "terraform_remote_state" "rds" {
  backend   = "s3"
  workspace = "csfeer-rds"

  config = {
    bucket = "${var.tf_state_bucket}"
    key    = "${var.environment_name}/state.tfstate"
    region = var.aws_region
  }
}
# Gets the csfeer VPC
data "aws_vpc" "csfeer_vpc" {
  filter {
    name   = "tag:Name"
    values = ["csfeer-${var.environment_name}-vpc"]
  }
}

# Gets all the private subnets in the csfeer VPC
data "aws_subnets" "csfeer_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.csfeer_vpc.id]
  }
  filter {
    name   = "tag:Tier"
    values = ["Private"]
  }
}

# Gets the csfeer EKS Cluster
data "aws_eks_cluster" "csfeer_eks_cluster" {
  name = "csfeer-${var.environment_name}"
}

# Gets the csfeer EKS OIDC Prov  ider
data "aws_iam_openid_connect_provider" "csfeer_eks_oidc_provider" {
  url = data.aws_eks_cluster.csfeer_eks_cluster.identity[0].oidc[0].issuer
}
