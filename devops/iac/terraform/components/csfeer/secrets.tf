## External API Secrets

## Tools and Services
resource "aws_secretsmanager_secret" "argo_cd_admin_password" {
  name        = "${local.name_prefix}/argo-cd/admin-password"
  description = "ArgoCD Admin Password"
  kms_key_id  = aws_kms_alias.key_alias.id
}


resource "aws_secretsmanager_secret" "app_secret_key" {
  name        = "${local.name_prefix}/api-secret-key"
  description = "API Secret key for signing sessions in the application"
  kms_key_id  = aws_kms_alias.key_alias.id
}

resource "aws_secretsmanager_secret" "oidc_client_secret" {
  name        = "${local.name_prefix}/oidc-client-secret"
  description = "OIDC Client Secret for the application"
  kms_key_id  = aws_kms_alias.key_alias.id
}

resource "aws_secretsmanager_secret" "auth_api_key" {
  name        = "${local.name_prefix}/auth-api-key"
  description = "Auth API Key for the application"
  kms_key_id  = aws_kms_alias.key_alias.id
}

resource "aws_secretsmanager_secret" "case_api_key" {
  name        = "${local.name_prefix}/case-api-key"
  description = "Case API Key for the application"
  kms_key_id  = aws_kms_alias.key_alias.id
}