variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "csfeer"
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnet IDs for ALB"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for ECS tasks"
  type        = list(string)
}

variable "db_host" {
  description = "Database host"
  type        = string
}

variable "db_name" {
  description = "Database name for Keycloak"
  type        = string
  default     = "keycloak"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "csfeer_admin"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "keycloak_admin_user" {
  description = "Keycloak admin username"
  type        = string
  default     = "admin"
}

variable "keycloak_admin_password" {
  description = "Keycloak admin password"
  type        = string
  sensitive   = true
  default     = "admin"
}

variable "oidc_client_secret" {
  description = "OIDC client secret for csfeer-auth client"
  type        = string
  sensitive   = true
  default     = "shhhhhhhh"
}

variable "task_cpu" {
  description = "Task CPU units"
  type        = string
  default     = "512"
}

variable "task_memory" {
  description = "Task memory in MB"
  type        = string
  default     = "1024"
}

variable "ecs_security_group_id" {
  description = "Security group ID of the CSFEER ECS tasks (to allow access)"
  type        = string
}

variable "rds_security_group_id" {
  description = "Security group ID of RDS (to allow Keycloak access)"
  type        = string
  default     = ""
}
