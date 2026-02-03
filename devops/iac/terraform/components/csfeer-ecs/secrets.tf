# AWS Secrets Manager Configuration
# This file manages secrets for the CSFeer application

# Application Secrets (Django SECRET_KEY, OIDC secrets, API keys, etc.)
resource "aws_secretsmanager_secret" "app_secrets" {
  name        = "${var.project_name}-${var.environment}-secrets"
  description = "Application secrets for CSFeer ${var.environment} environment"

  recovery_window_in_days = var.secret_recovery_days

  tags = {
    Name        = "${var.project_name}-${var.environment}-secrets"
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Application Secret Values
# Note: These are populated with initial values from Terraform variables
# In production, you should rotate these secrets regularly using AWS Secrets Manager rotation
resource "aws_secretsmanager_secret_version" "app_secrets" {
  secret_id = aws_secretsmanager_secret.app_secrets.id

  secret_string = jsonencode({
    SECRET_KEY           = var.django_secret_key
    OIDC_CLIENT_SECRET   = var.oidc_client_secret
    API_KEY              = var.api_key
    DEBUG                = var.django_debug
    ALLOWED_HOSTS        = var.allowed_hosts
    CSRF_TRUSTED_ORIGINS = var.csrf_trusted_origins
  })

  lifecycle {
    ignore_changes = [
      secret_string, # Ignore changes after initial creation (allows manual updates)
    ]
  }
}

# Database Credentials Secret
# Separate secret for database credentials following AWS best practices
resource "aws_secretsmanager_secret" "db_credentials" {
  name        = "${var.project_name}-${var.environment}-db-credentials"
  description = "Database credentials for CSFeer ${var.environment} RDS instance"

  recovery_window_in_days = var.secret_recovery_days

  tags = {
    Name        = "${var.project_name}-${var.environment}-db-credentials"
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Database Secret Values
# Schema matches AWS RDS automatic secret format for easier migration
resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id

  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    host     = var.db_host
    port     = 5432
    dbname   = var.db_name
    engine   = "postgres"
  })

  lifecycle {
    ignore_changes = [
      secret_string, # Ignore changes after initial creation (allows manual rotation)
    ]
  }
}

# Optional: Enable automatic rotation for database credentials
# Requires a Lambda function to perform the rotation
# Uncomment and configure when ready for production
#
# resource "aws_secretsmanager_secret_rotation" "db_credentials" {
#   secret_id           = aws_secretsmanager_secret.db_credentials.id
#   rotation_lambda_arn = aws_lambda_function.rotate_db_secret.arn
#
#   rotation_rules {
#     automatically_after_days = 30
#   }
# }
