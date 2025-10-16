locals {
  # removes the decimal point and minor version number
  # i.e. 11.5 -> 11
  pg_family_suffix = replace(var.engine_version, "/\\.\\d*$/", "")

  ## Available options: auto_explain,orafce,pgaudit,pg_ad_mapping,pg_bigm,pg_similarity,pg_stat_statements,pg_tle,pg_hint_plan,pg_prewarm,plprofiler,pglogical,pg_cron
  default_preload_libraries = "pg_stat_statements,pgaudit"
  optional_preload_library  = var.enable_pg_cron ? ",pg_cron" : ""

  default_psql_cluster_parameters = {
    log_autovacuum_min_duration = { value = 10001 } # 10001 instead of 10000 since setting the default value results in Terraform not tracking this parameter in the state file, making it think this is always a proposed change.
    log_connections             = { value = 1 }
    log_disconnections          = { value = 1 }
    log_lock_waits              = { value = 1 }
    log_temp_files              = { value = 0 }
    log_statement               = { value = "none" }
    log_error_verbosity         = { value = "terse" }
    log_min_error_statement     = { value = "log" }
    log_rotation_age            = { value = 1440 }
    "pgaudit.log"               = { value = "DDL" }
    "pgaudit.role"              = { value = "rds_pgaudit" }
    "rds.log_retention_period"  = { value = 10080 }
    "shared_preload_libraries"  = { value = "${local.default_preload_libraries}${local.optional_preload_library}", apply_method = "pending-reboot" }
    "rds.force_ssl"             = { value = 1 }

  }

  cluster_parameters = merge(
    local.default_psql_cluster_parameters,
    var.cluster_parameters
  )
}

resource "aws_rds_cluster_parameter_group" "cluster" {
  name   = local.cluster_identifier
  family = "${var.engine}${local.pg_family_suffix}"

  dynamic "parameter" {
    for_each = local.cluster_parameters
    content {
      name         = parameter.key
      value        = parameter.value["value"]
      apply_method = lookup(parameter.value, "apply_method", "immediate")
    }
  }
}
