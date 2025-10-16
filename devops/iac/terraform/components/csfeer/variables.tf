variable "tf_state_bucket" {
  description = "The name of the S3 bucket used to store Terraform state files."
}

variable "aws_region" {
  description = "The AWS region where the infrastructure will be deployed."
  type        = string
}

variable "environment_name" {
  description = "The name of the environment where the infrastructure will be deployed. This can be 'dev', 'stage', or 'prod'."
  type        = string
}

variable "domain_names" {
  description = "A list of domain names that will be used for the CloudFront distribution. This is optional."
  type        = list(string)
  default     = []
}

variable "certificate_arn" {
  description = "The ARN of the ACM certificate used for SSL/TLS encryption."
  type        = string
  default     = ""
}
variable "backend_alb_arn" {
  description = "The ARN of the Elastic Load Balancer (ELB) that serves as the VPC origin."
  type        = string
  default     = ""
}
variable "backend_alb_name" {
  description = "The name of the Elastic Load Balancer (ELB) that serves as the VPC origin."
  type        = string
  default     = ""
}
variable "oidc_provider_url" {
  description = "The URL of the OIDC provider used for authentication in the EKS cluster. This is optional."
  type        = string
  default     = null
}

variable "backend_elb_protocol" {
  description = "The protocol of the Elastic Load Balancer (ELB) that serves as the origin for the backend application."
  type        = string
  default     = "HTTPS"
}

variable "vpc_id" {
  description = "The ID of the VPC where the infrastructure will be deployed. This is optional."
  type        = string
  default     = ""
}

variable "eks_cluster_security_group_id" {
  description = "The ID of the security group associated with the EKS cluster. This is optional."
  type        = string
  default     = ""
}

variable "application_name" {
  description = "The name of the application being deployed."
  type        = string
  default     = "csfeer"
}

variable "disable_allow_ip_waf" {
  description = "A flag to disable the AWS WAF ACL that limits IP addresses that can access the CloudFront distribution."
  type        = bool
  default     = false
}

variable "cloudwatch_error_notification_emails" {
  description = "A list of email addresses to notify when the CloudWatch alarm is triggered."
  type        = list(string)
  default     = []
}

variable "cloudwatch_log_group_name" {
  description = "The name of the CloudWatch log group to use for the application."
  type        = string
  default     = ""
}

variable "create_shared_secrets" {
  description = "A flag to create a shared secrets and KMS key. We need to create the secrets only once per account."
  type        = bool
  default     = true
}
