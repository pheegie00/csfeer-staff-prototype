environment_name = "dev"
aws_region = "us-east-1"
tf_state_bucket = "csfeer-dev-tf-state-us-east-1"
# These are the variables that are required for the csfeer API component DEV environment.

#Phase 1: required! 


oidc_provider_url             = "FILL IN"
# Security group ID of the EKS cluster so we can allow the EKS cluster to access the Redis cluster.
eks_cluster_security_group_id = "FILL IN"

# CloudWatch log group name.
cloudwatch_error_notification_emails = []

# Phase 2: The following variables are settings.

## Uncomment the following variables once we have a DNS updated in CloudFlare.
# cloudfront_alias              = []
# cloudfront_certificate_arn    = "FILL IN"

# Uncomment the following variables once the alb is created from argocd
# The ARN of the ALB for the VPC origin.
# backend_alb_arn  = 
# backend_alb_name = 

# The protocol of the Elastic Load Balancer (ELB) that serves as the origin for the backend application. Use HTTP if we dont have a certificate yet.
backend_elb_protocol = "HTTP"