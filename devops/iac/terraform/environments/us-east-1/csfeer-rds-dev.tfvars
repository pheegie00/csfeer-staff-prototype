environment_name = "dev"
aws_region = "us-east-1"
tf_state_bucket = "csfeer-dev-tf-state-us-east-1"
# These are the variables that are required for the csfeer API component DEV environment.
backup_retention_period        = 7
cloudwatch_notification_emails = []
vpc_id                         = "FILL IN"
subnet_ids                     = ["FILL IN"]
cluster_security_group_id      = "FILL IN"
