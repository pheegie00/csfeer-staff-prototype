locals {
  key_administration_principals = [
    "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root",
    "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/terragrunter",
    "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_AWSOrganizationsFullAccess_a5b3b4360b25f4ad"
  ]

  key_users_principals = [
    "${aws_iam_role.csfeer_app_role.arn}",
    "${aws_iam_role.csfeer_db_migration_role.arn}"
  ]
}

# KMS Key to encrypt secrets that can be used by current environment
resource "aws_kms_key" "csfeer_kms_key" {
  description                        = "KMS key for csfeer"
  enable_key_rotation                = true
  deletion_window_in_days            = 7
  bypass_policy_lockout_safety_check = false # Don't let us create immortal/unmanageable keys.
  policy = jsonencode({
    Version = "2012-10-17"
    # Put default policies first so IAM document diff is minimized due to alphabetization of user-supplied stanza keys.
    Statement = concat(
      [{
        Sid      = "AllowAdministrators"
        Effect   = "Allow"
        Action   = "kms:*"
        Resource = "*"
        Principal = {
          AWS = local.key_administration_principals
        }
        },
        {
          Sid    = "Allow use of the key"
          Effect = "Allow"
          Action = [
            "kms:Encrypt",
            "kms:Decrypt",
            "kms:ReEncrypt*",
            "kms:GenerateDataKey*",
            "kms:DescribeKey"
          ]
          Resource = "*"
          Principal = {
            AWS = local.key_users_principals
          }
        },
        {
          Sid    = "Allow CloudWatch Alarms to publish to encrypted SNS topics"
          Effect = "Allow"
          Principal = {
            Service = "cloudwatch.amazonaws.com"
          }
          Action = [
            "kms:GenerateDataKey",
            "kms:Decrypt"
          ]
          Resource = "*"
          Condition = {
            StringEquals = {
              "aws:SourceAccount" = data.aws_caller_identity.current.account_id
            }
            ArnLike = {
              "aws:SourceArn" = "arn:aws:cloudwatch:${var.aws_region}:${data.aws_caller_identity.current.account_id}:alarm:${local.name_prefix}-*" # Allow CloudWatch Alarms to publish to encrypted SNS topics
            }
          }
        },
        {
          Sid    = "Allow attachment of persistent resources"
          Effect = "Allow"
          Action = [
            "kms:CreateGrant",
            "kms:ListGrants",
            "kms:RevokeGrant"
          ]
          Resource = "*"
          Principal = {
            AWS = local.key_users_principals
          }
          Condition = {
            Bool = {
              "kms:GrantIsForAWSResource" = "true"
            }
          }
        }
      ]
    )
  })
}

resource "aws_kms_alias" "key_alias" {
  name          = "alias/${local.name_prefix}-key"
  target_key_id = aws_kms_key.csfeer_kms_key.key_id
}

# KMS Key for Shared Secrets that can be used by all environments
resource "aws_kms_key" "shared_secrets_kms_key" {
  count                              = var.create_shared_secrets ? 1 : 0
  description                        = "KMS key for Shared Secrets"
  enable_key_rotation                = true
  deletion_window_in_days            = 7
  bypass_policy_lockout_safety_check = false # Don't let us create immortal/unmanageable keys.
  policy = jsonencode({
    Version = "2012-10-17"
    # Put default policies first so IAM document diff is minimized due to alphabetization of user-supplied stanza keys.
    Statement = concat(
      [{
        Sid      = "AllowAdministrators"
        Effect   = "Allow"
        Action   = "kms:*"
        Resource = "*"
        Principal = {
          AWS = local.key_administration_principals
        }
        },
        {
          Sid    = "Allow use of the key"
          Effect = "Allow"
          Action = [
            "kms:Encrypt",
            "kms:Decrypt",
            "kms:ReEncrypt*",
            "kms:GenerateDataKey*",
            "kms:DescribeKey"
          ]
          Resource = "*"
          Principal = {
            AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
          }
          Condition = {
            StringEquals = {
              "aws:PrincipalArn" = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/sandbox/csfeer*"
            }
          }
        },
        {
          Sid    = "Allow attachment of persistent resources"
          Effect = "Allow"
          Action = [
            "kms:CreateGrant",
            "kms:ListGrants",
            "kms:RevokeGrant"
          ]
          Resource = "*"
          Principal = {
            AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"

          }
          Condition = {
            Bool = {
              "kms:GrantIsForAWSResource" = "true"
            }
            StringEquals = {
              "aws:PrincipalArn" = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/sandbox/csfeer*"
            }
          }
        }
      ]
    )
  })
}

resource "aws_kms_alias" "shared_secrets_key_alias" {
  count         = var.create_shared_secrets ? 1 : 0
  name          = "alias/${var.application_name}-shared-key"
  target_key_id = aws_kms_key.shared_secrets_kms_key[0].key_id
}
