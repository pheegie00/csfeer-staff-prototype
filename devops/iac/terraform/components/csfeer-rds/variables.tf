variable "tf_state_bucket" {
  description = "state bucket"
}

variable "aws_region" {
  description = "The region to deploy to"
  type        = string
}

variable "environment_name" {
  description = "The environment to deploy to. (dev | stage | prod)"
  type        = string
}

variable "csfeer_snapshot_identifier" {
  default = ""
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "instance_count" {
  default     = 1
  type        = number
  description = "Number of Aurora instances to create"
}

variable "allocated_storage" {
  description = "RDS allocated storage GB"
  type        = string
  default     = "20"
}
variable "backup_retention_period" {
  description = "RDS backup retention period"
  type        = string
  default     = 30
}

variable "security_group_ids" {
  description = "Security Group IDs to allow access"
  type        = list(string)
  default     = []
}

variable "cloudwatch_notification_emails" {
  description = "Email address to send cloudwatch notifications to"
  type        = list(string)
}

variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
  default     = null
}

variable "subnet_ids" {
  description = "List of subnet IDs for the RDS instance"
  type        = list(string)
  default     = null
}

variable "cluster_security_group_id" {
  description = "The ID of the EKS cluster security group"
  type        = string
  default     = null
}

variable "performance_insights_enabled" {
  description = "Enable performance insights"
  type        = bool
  default     = true
}
