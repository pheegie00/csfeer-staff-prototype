output "endpoint" {
  value       = aws_rds_cluster.rds_aurora_cluster.endpoint
  description = "The endpoint of the RDS instance"
}

output "endpoint_read_only" {
  value       = aws_rds_cluster.rds_aurora_cluster.reader_endpoint
  description = "The read-only endpoint of the RDS instance"
}

output "cluster_resource_id" {
  value       = aws_rds_cluster.rds_aurora_cluster.cluster_resource_id
  description = "The region-unique, immutable identifier for the RDS cluster."
}

output "master_username" {
  value       = aws_rds_cluster.rds_aurora_cluster.master_username
  description = "The master username for the database"
}

output "master_password_secret_arn" {
  value       = aws_rds_cluster.rds_aurora_cluster.master_user_secret
  description = "The ARN of the master password in secret manager"
}

output "database_name" {
  value       = aws_rds_cluster.rds_aurora_cluster.database_name
  description = "The database name"
}
