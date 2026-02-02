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
  description = "VPC ID where RDS will be created"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for RDS (need at least 2 in different AZs)"
  type        = list(string)
}

variable "postgres_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "15.8"
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "Initial storage in GB"
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Maximum storage in GB (enables autoscaling)"
  type        = number
  default     = 100
}

variable "storage_type" {
  description = "Storage type"
  type        = string
  default     = "gp3"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "csfeer"
}

variable "db_username" {
  description = "Master username"
  type        = string
  default     = "csfeer_admin"
}

variable "db_password" {
  description = "Master password"
  type        = string
  sensitive   = true
}

variable "publicly_accessible" {
  description = "Make RDS publicly accessible (not recommended for production)"
  type        = bool
  default     = false
}

variable "backup_retention_period" {
  description = "Backup retention period in days (0 for free tier compatibility)"
  type        = number
  default     = 0
}

variable "backup_window" {
  description = "Backup window"
  type        = string
  default     = "03:00-04:00"
}

variable "maintenance_window" {
  description = "Maintenance window"
  type        = string
  default     = "mon:04:00-mon:05:00"
}

variable "multi_az" {
  description = "Enable multi-AZ deployment"
  type        = bool
  default     = false
}

variable "skip_final_snapshot" {
  description = "Skip final snapshot on destroy (use true for dev)"
  type        = bool
  default     = true
}

variable "deletion_protection" {
  description = "Enable deletion protection"
  type        = bool
  default     = false
}

variable "enable_performance_insights" {
  description = "Enable Performance Insights (not available on free tier)"
  type        = bool
  default     = false
}
