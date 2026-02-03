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
  description = "VPC ID where resources will be created"
  type        = string
}

variable "public_subnet_ids" {
  description = "Public subnet IDs for ALB"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for ECS tasks (or use public if no NAT)"
  type        = list(string)
}

variable "ecr_image_uri" {
  description = "ECR image URI for the application"
  type        = string
}

variable "db_host" {
  description = "Database host endpoint"
  type        = string
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "csfeer"
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

variable "django_secret_key" {
  description = "Django SECRET_KEY"
  type        = string
  sensitive   = true
}

variable "django_debug" {
  description = "Django DEBUG setting"
  type        = string
  default     = "False"
}

variable "allowed_hosts" {
  description = "Django ALLOWED_HOSTS (JSON array format)"
  type        = string
  default     = "[\"*\"]"
}

variable "csrf_trusted_origins" {
  description = "Django CSRF_TRUSTED_ORIGINS (JSON array format)"
  type        = string
  default     = "[]"
}

variable "use_oidc" {
  description = "Enable OIDC authentication (set to false for Django auth)"
  type        = string
  default     = "true"
}

variable "oidc_document_url" {
  description = "OIDC Discovery Document URL"
  type        = string
  default     = ""
}

# Task configuration
variable "task_cpu" {
  description = "Task CPU units (256 = 0.25 vCPU)"
  type        = string
  default     = "256"
}

variable "task_memory" {
  description = "Task memory in MB"
  type        = string
  default     = "512"
}

variable "desired_count" {
  description = "Desired number of tasks"
  type        = number
  default     = 1
}

variable "container_port" {
  description = "Container port"
  type        = number
  default     = 8000
}

# Health check configuration
variable "health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/admin/login/"
}

variable "health_check_interval" {
  description = "Health check interval in seconds"
  type        = number
  default     = 30
}

variable "health_check_timeout" {
  description = "Health check timeout in seconds"
  type        = number
  default     = 5
}

variable "health_check_healthy_threshold" {
  description = "Healthy threshold count"
  type        = number
  default     = 2
}

variable "health_check_unhealthy_threshold" {
  description = "Unhealthy threshold count"
  type        = number
  default     = 3
}

# Logging
variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 7
}

# Features
variable "enable_execute_command" {
  description = "Enable ECS Exec for debugging"
  type        = bool
  default     = true
}

variable "assign_public_ip" {
  description = "Assign public IP to tasks (required if no NAT gateway)"
  type        = bool
  default     = true
}

# AWS Secrets Manager Configuration
variable "use_secrets_manager" {
  description = "Enable AWS Secrets Manager for storing sensitive configuration"
  type        = bool
  default     = true
}

variable "secret_recovery_days" {
  description = "Number of days to retain deleted secrets (0-30, 0 = immediate deletion)"
  type        = number
  default     = 7
}

variable "oidc_client_secret" {
  description = "OIDC client secret for authentication"
  type        = string
  sensitive   = true
  default     = ""
}

variable "api_key" {
  description = "API key for application"
  type        = string
  sensitive   = true
  default     = "SECRET123"
}
