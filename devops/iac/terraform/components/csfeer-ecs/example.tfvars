# Example terraform.tfvars for csfeer-ecs component
# Copy this file to terraform.tfvars and fill in your values

environment         = "dev"
aws_region          = "us-east-1"
project_name        = "csfeer"

# Network configuration
vpc_id              = "vpc-xxxxx"
public_subnet_ids   = ["subnet-aaa", "subnet-bbb"]
private_subnet_ids  = ["subnet-xxx", "subnet-yyy"]

# Container configuration
ecr_image_uri       = "123456789012.dkr.ecr.us-east-1.amazonaws.com/csfeer:dev"

# Database connection (from RDS deployment)
db_host             = "csfeer-dev-db.xxxxx.us-east-1.rds.amazonaws.com"
db_name             = "csfeer"
db_username         = "csfeer_admin"
db_password         = "your-secure-password-here"

# Django configuration
django_secret_key   = "your-django-secret-key-here"
django_debug        = "False"
allowed_hosts       = "*"

# Task configuration (optional overrides)
task_cpu            = "256"   # 0.25 vCPU
task_memory         = "512"   # 0.5 GB
desired_count       = 1

# Features
enable_execute_command = true
assign_public_ip       = true
