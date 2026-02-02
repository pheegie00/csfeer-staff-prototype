# Example terraform.tfvars for csfeer-rds-simple component
# Copy this file to terraform.tfvars and fill in your values

environment  = "dev"
aws_region   = "us-east-1"
project_name = "csfeer"

# Network configuration
vpc_id       = "vpc-xxxxx"
subnet_ids   = ["subnet-xxx", "subnet-yyy"]

# Database configuration
postgres_version = "15.8"
instance_class   = "db.t3.micro"
allocated_storage = 20

# Generate secure password with: openssl rand -base64 32
db_password = "your-secure-password-here"

# Optional overrides
db_name     = "csfeer"
db_username = "csfeer_admin"
multi_az    = false

# Dev settings
skip_final_snapshot = true
deletion_protection = false
