## ---------------------------------------------------------------------------------------------------------------------
## ONE LINE SUMMARY DESCRIBING WHAT IS BEING MANAGED IN THIS SECTION IN ALL CAPS
## The rest of the comments should be in standard casing. This section should contain an overall description of the
## component that is being managed, and highlight any unconventional workarounds or configurations that are in place.
## ---------------------------------------------------------------------------------------------------------------------


output "csfeer_db_migration_role" {
  description = "The ARN of the role that will be used to perform the database migration"
  value       = aws_iam_role.csfeer_db_migration_role.arn
}

output "csfeer_app_role" {
  value       = aws_iam_role.csfeer_app_role.arn
  description = "The ARN of the role that will be assumed by the csfeer App"
}

output "csfeer_kms_key_alias" {
  description = "The alias of the KMS key"
  value       = aws_kms_alias.key_alias.name
}

output "csfeer_kms_key_id" {
  description = "The ID of the KMS key"
  value       = aws_kms_key.csfeer_kms_key.key_id
}
