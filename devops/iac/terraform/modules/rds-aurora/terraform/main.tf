/**
* tf-rds-aurora
*
* Creates an RDS Aurora Cluster with instances.
*
*/

locals {
  cluster_identifier = "${var.application_name}-${var.environment_name}"
}

resource "aws_rds_cluster" "rds_aurora_cluster" {
  cluster_identifier                  = "${local.cluster_identifier}-rds"
  engine                              = var.engine
  engine_version                      = var.engine_version
  db_subnet_group_name                = aws_db_subnet_group.rds_subnet_group.name
  database_name                       = var.database_name
  master_username                     = var.master_username
  manage_master_user_password         = true
  iam_database_authentication_enabled = var.iam_database_authentication_enabled
  port                                = var.db_port
  db_cluster_parameter_group_name     = aws_rds_cluster_parameter_group.cluster.id
  final_snapshot_identifier           = "${local.cluster_identifier}-${replace(var.engine_version, ".", "")}-final"
  backup_retention_period             = var.backup_retention_period
  storage_encrypted                   = true
  deletion_protection                 = true
  vpc_security_group_ids              = [aws_security_group.rds_security_group.id]
  skip_final_snapshot                 = true
  enabled_cloudwatch_logs_exports     = var.log_forwarding_enabled ? var.enabled_cloudwatch_logs_exports : []
  copy_tags_to_snapshot               = true
}

# Have to define engine and engine_version in the cluster instance resource too
# Else the instance will default to a mismatched version
# https://github.com/terraform-providers/terraform-provider-aws/issues/4779
resource "aws_rds_cluster_instance" "cluster_instances" {
  count                                 = var.instance_count
  identifier                            = "${local.cluster_identifier}-instance-${count.index}"
  cluster_identifier                    = aws_rds_cluster.rds_aurora_cluster.id
  engine                                = var.engine
  engine_version                        = var.engine_version
  instance_class                        = var.instance_class
  performance_insights_enabled          = var.performance_insights_enabled
  performance_insights_retention_period = var.performance_insights_enabled ? var.performance_insights_retention_period : null
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${local.cluster_identifier}-rds-aurora"
  subnet_ids = var.subnet_ids
}

data "aws_region" "current" {}

resource "aws_security_group" "rds_security_group" {
  description = "RDS"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  dynamic "ingress" {
    for_each = var.security_group_ids
    content {
      description     = ""
      from_port       = var.db_port
      to_port         = var.db_port
      protocol        = "tcp"
      security_groups = [ingress.value]
      self            = true
    }
  }

  ingress {
    description = ""
    from_port   = var.db_port
    to_port     = var.db_port
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidrs
  }

  name_prefix = "${local.cluster_identifier}-rds-security-group"

  vpc_id = var.vpc_id

  lifecycle {
    create_before_destroy = true
  }
}
