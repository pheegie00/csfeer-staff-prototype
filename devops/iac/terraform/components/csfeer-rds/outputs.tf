## ---------------------------------------------------------------------------------------------------------------------
## ONE LINE SUMMARY DESCRIBING WHAT IS BEING MANAGED IN THIS SECTION IN ALL CAPS
## The rest of the comments should be in standard casing. This section should contain an overall description of the
## component that is being managed, and highlight any unconventional workarounds or configurations that are in place.
## ---------------------------------------------------------------------------------------------------------------------

# output the db endpoint
output "rds_endpoint" {
  value       = element(split(":", module.csfeer_rds_aurora.endpoint), 0)
  description = "The endpoint of the RDS instance"
}

# output the dbname
output "rds_dbname" {
  value       = module.csfeer_rds_aurora.database_name
  description = "The database name"
}

# output the master username
output "rds_master_username" {
  value       = module.csfeer_rds_aurora.master_username
  description = "The master username"
}

# output the master password location in secret manager
output "rds_master_password_secret" {
  value       = module.csfeer_rds_aurora.master_password_secret_arn
  description = "The master password secret ARN"
}

output "rds_cluster_identifier" {
  value       = module.csfeer_rds_aurora.cluster_resource_id
  description = "The RDS Cluster Identifier"
}