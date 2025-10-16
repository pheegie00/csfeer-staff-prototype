environment_name = "dev"
aws_region       = "us-east-1"
tf_state_bucket  = "csfeer-dev-tf-state-us-east-1"
# These are the variables that are required for the csfeer API component DEV environment.

app_helm_chart_version = "FILL IN"
app_helm_values_files  = ["values.yaml", "values-dev.yaml"] # Order of value files is important, the first value file should always be the values.yaml file
create_namespace       = true
prune                  = true

