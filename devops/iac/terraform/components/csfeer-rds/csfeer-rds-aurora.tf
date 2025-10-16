locals {
  db_name            = "csfeer"
  db_master_username = "csfeer_master"
  db_port            = 5432
  application_name   = "csfeer"
  schema_name        = "public"
}

resource "aws_sns_topic" "cloudwatch_notification_aurora" {
  name              = "${local.application_name}-${var.environment_name}-rds-cloudwatch"
  kms_master_key_id = can(data.terraform_remote_state.csfeer.outputs.csfeer_kms_key_alias) ? data.terraform_remote_state.csfeer.outputs.csfeer_kms_key_alias : null
}

resource "aws_sns_topic_subscription" "cloudwatch_notification_aurora_subscription" {
  for_each  = toset(var.cloudwatch_notification_emails)
  topic_arn = aws_sns_topic.cloudwatch_notification_aurora.arn
  protocol  = "email"
  endpoint  = each.value
}

module "csfeer_rds_aurora" {
  source = "../../../terraform/modules/rds-aurora/terraform"

  vpc_id                              = var.vpc_id != null ? var.vpc_id : data.aws_vpc.csfeer_vpc.id
  subnet_ids                          = var.subnet_ids != null ? var.subnet_ids : data.aws_subnets.csfeer_subnets.ids
  security_group_ids                  = concat(var.security_group_ids, [var.cluster_security_group_id])
  allowed_cidrs                       = ["172.40.0.0/16"] # AWS Client VPN
  instance_count                      = var.instance_count
  environment_name                    = var.environment_name
  cloudwatch_notification_arn         = aws_sns_topic.cloudwatch_notification_aurora.arn
  database_name                       = local.db_name
  master_username                     = local.db_master_username
  engine                              = "aurora-postgresql"
  engine_version                      = "16.6"
  db_port                             = 5432
  instance_class                      = var.db_instance_class
  snapshot_identifier                 = var.csfeer_snapshot_identifier
  backup_retention_period             = var.backup_retention_period
  performance_insights_enabled        = var.performance_insights_enabled
  iam_database_authentication_enabled = true
  application_name                    = local.application_name
  enabled_cloudwatch_logs_exports     = ["postgresql"]
  log_forwarding_enabled              = true
}
