# TODO: Improve this to limit access to the secrets needed only 
locals {
  db_users = {
    app_user = "csfeer_app_user"
    reader_user = "csfeer_reader_user"
    admin_user = "csfeer_admin_user"
    migration_user = "csfeer_migration_user"
  }
  name_prefix     = "${var.application_name}-${var.environment_name}"
  redis_user_name = "${local.name_prefix}-redis-user"
}

# This is the role used by the application to access the database, ses, secrets and others
resource "aws_iam_role" "csfeer_app_role" {
  name        = "${local.name_prefix}-app-iam-role"
  path        = "/sandbox/"
  description = "Role used by the application to access AWS resources"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = var.oidc_provider_url != null ? var.oidc_provider_url : data.aws_iam_openid_connect_provider.csfeer_eks_oidc_provider.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        # Condition = {
        #   StringEquals = {
        #     "${local.oidc_provider_url}:sub" = "system:serviceaccount:csfeer:csfeer"
        #     "${local.oidc_provider_url}:aud" = "sts.amazonaws.com"
        #   }
        # }
      }
    ]
  })
}

## Crete a IAM Role for Keycloak (Temporary Okta solution)

# Get the rds auto generated password aws:rds:primaryDBClusterArn
# data "aws_secretsmanager_secret" "keycloak_db_password" {
#   name = "arn:aws:rds:${var.aws_region}:${data.aws_caller_identity.current.account_id}:cluster:${local.name_prefix}-rds"
#   tags = {
#     "aws:rds:primaryDBClusterArn" = "arn:aws:rds:${var.aws_region}:${data.aws_caller_identity.current.account_id}:cluster:${local.name_prefix}-rds"
#     "aws:secretsmanager:owningService" = "rds"
#   }
# }
resource "aws_iam_role" "keycloak_role" {
  name        = "${local.name_prefix}-keycloak-iam-role"
  path        = "/sandbox/"
  description = "Role used by Keycloak to access AWS resources"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = var.oidc_provider_url != null ? var.oidc_provider_url : data.aws_iam_openid_connect_provider.csfeer_eks_oidc_provider.arn
        }
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resources = [
          "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:${local.name_prefix}/keycloak/*",
         // data.aws_secretsmanager_secret.keycloak_db_password.arn
        ]
      }
    ]
  })
}



### Secrets Manager

# We will get the shared kms key if we are not creating the shared secrets in this environment.
data "aws_kms_key" "shared_secrets_kms_key" {
  count  = var.create_shared_secrets ? 0 : 1 # This is reversed, we get the shared kms key but if we creating it then we reference it.
  key_id = "alias/${var.application_name}-shared-key"
}


data "aws_iam_policy_document" "secrets_manager_policy" {
  statement {
    effect = "Allow"
    actions = ["secretsmanager:GetSecretValue",
    "secretsmanager:DescribeSecret"]
    resources = [
      "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:${local.name_prefix}/*",
      "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:${var.application_name}/shared/*"
    ]
  }
  statement {
    effect  = "Allow"
    actions = ["kms:Decrypt"]
    resources = [
      aws_kms_key.csfeer_kms_key.arn,
      var.create_shared_secrets ? aws_kms_key.shared_secrets_kms_key[0].arn : data.aws_kms_key.shared_secrets_kms_key[0].arn
    ]
  }
}

resource "aws_iam_policy" "secrets_manager_policy" {
  name        = "${local.name_prefix}-secrets-manager-policy"
  path        = "/sandbox/"
  description = "IAM policy for accessing secrets in Secrets Manager"
  policy      = data.aws_iam_policy_document.secrets_manager_policy.json
}


resource "aws_iam_role_policy_attachment" "secrets_policy_attachment" {
  role       = aws_iam_role.csfeer_app_role.name
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}


#### RDS Database

data "aws_iam_policy_document" "rds_connect_policy" {
  for_each = local.db_users

  statement {
    effect  = "Allow"
    actions = ["rds-db:connect"]
    resources = [
      "arn:aws:rds-db:${var.aws_region}:${data.aws_caller_identity.current.account_id}:dbuser:${data.terraform_remote_state.rds.outputs.rds_cluster_identifier}/${each.value}"
    ]
  }
}

resource "aws_iam_policy" "rds_connect_policy" {
  for_each    = local.db_users
  name        = "${local.name_prefix}-rds-connect-policy-${each.value}"
  path        = "/sandbox/"
  description = "IAM policy for RDS IAM authentication for ${each.value}"
  policy      = data.aws_iam_policy_document.rds_connect_policy[each.key].json
}

resource "aws_iam_role_policy_attachment" "rds_connect_policy_attachment_app" {
  role       = aws_iam_role.csfeer_app_role.name
  policy_arn = aws_iam_policy.rds_connect_policy["app_user"].arn
}

## RDS DB Migration Role
resource "aws_iam_role" "csfeer_db_migration_role" {
  name        = "${local.name_prefix}-rds-db-migration-role"
  path        = "/sandbox/"
  description = "Role used by csfeer Container to execute RDS DB Migration"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = var.oidc_provider_url != null ? var.oidc_provider_url : data.aws_iam_openid_connect_provider.csfeer_eks_oidc_provider.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "rds_connect_policy_attachment_migrate" {
  role       = aws_iam_role.csfeer_db_migration_role.name
  policy_arn = aws_iam_policy.rds_connect_policy["migration_user"].arn
}

### ElasticCache Redis Connection

data "aws_iam_policy_document" "elasticache_redis_connection" {
  statement {
    effect  = "Allow"
    actions = ["elasticache:Connect"]
    resources = [
      "arn:aws:elasticache:${var.aws_region}:${data.aws_caller_identity.current.account_id}:serverlesscache:${local.name_prefix}-redis-cluster",
      "arn:aws:elasticache:${var.aws_region}:${data.aws_caller_identity.current.account_id}:user:${local.redis_user_name}"
    ]
  }
}

resource "aws_iam_policy" "elasticache_redis_connection_policy" {
  name        = "${local.name_prefix}-elasticache-redis-connection-policy"
  path        = "/sandbox/"
  description = "IAM policy for ElasticCache Redis connection"
  policy      = data.aws_iam_policy_document.elasticache_redis_connection.json
}

resource "aws_iam_role_policy_attachment" "elasticache_redis_connection_policy_attachment" {
  role       = aws_iam_role.csfeer_app_role.name
  policy_arn = aws_iam_policy.elasticache_redis_connection_policy.arn
}

### SES Sending Email Permission

data "aws_iam_policy_document" "ses_send_email" {
  statement {
    effect = "Allow"
    actions = [
      "ses:SendEmail",
      "ses:SendRawEmail",
      "ses:SendCustomVerificationEmail",
      "ses:UpdateEmailTemplate",
      "ses:GetEmailTemplate",
      "ses:SendBulkEmail",
      "ses:GetEmailIdentity"
    ]
    resources = [
      "arn:aws:ses:${var.aws_region}:${data.aws_caller_identity.current.account_id}:identity/state.gov",
      "arn:aws:ses:${var.aws_region}:${data.aws_caller_identity.current.account_id}:configuration-set/${local.name_prefix}",
      "arn:aws:ses:${var.aws_region}:${data.aws_caller_identity.current.account_id}:template/${local.name_prefix}/*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "ses:GetAccount",
      "ses:ListEmailTemplates"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "ses_send_email_policy" {
  name        = "${local.name_prefix}-ses-policy"
  path        = "/sandbox/"
  description = "IAM policy for csfeer to send email with AWS SES"
  policy      = data.aws_iam_policy_document.ses_send_email.json
}

resource "aws_iam_role_policy_attachment" "ses_send_email_policy" {
  role       = aws_iam_role.csfeer_app_role.name
  policy_arn = aws_iam_policy.ses_send_email_policy.arn
}

resource "aws_iam_role_policy_attachment" "cloudwatch_agent_server_policy" {
  role       = aws_iam_role.csfeer_app_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}
