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


data "aws_vpc" "csfeer_vpc" {
  filter {
    name   = "tag:Name"
    values = ["csfeer-platform-${var.environment_name}-vpc"]
  }
}

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
