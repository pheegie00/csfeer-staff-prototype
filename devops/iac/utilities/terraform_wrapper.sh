#!/bin/bash
# Terraform Wrapper Script
#
# This script is a wrapper for Terraform operations, providing a standardized way to manage
# infrastructure across different environments, regions, and components.
#
# Usage:
#   ./terraform_wrapper.sh <component_name> <environment_type> <terraform_command> [<terraform_options>]
#
# Arguments:
#   <component_name>     : The name of the component to deploy (e.g., "csfeer", "csfeer-rds")
#   <environment_type>   : The environment to deploy to (e.g., "dev", "staging", "prod")
#   <terraform_command>  : The Terraform command to run (e.g., "plan", "apply", "destroy")
#   [<terraform_options>]: Optional additional Terraform command options
#
# Examples:
#   ./terraform_wrapper.sh csfeer dev plan
#
# Notes:
#   - This script assumes a specific directory structure for Terraform configurations.
#   - It automatically sets the appropriate AWS profile based on the environment.
#   - It uses environment-specific, region-specific, and component-specific variable files.
#   - The script requires Git to determine the repository root.
#   - You can set the environment variable `USE_AWS_PROFILE` to use a specific AWS profile.
#
# Requirements:
#   - Terraform must be installed and accessible in the system PATH.
#   - AWS CLI must be configured with the appropriate profiles.
#   - The script must be run from within the Git repository.

# Set default TERRAFORM_EXECUTABLE if not provided
TERRAFORM_EXECUTABLE="${TERRAFORM_EXECUTABLE:-terraform}"
echo "Executable: $TERRAFORM_EXECUTABLE Version:"
$TERRAFORM_EXECUTABLE -v

# Check if required arguments are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 [-s] <deployable_type> <deployable_name> <terraform_command> [<terraform_options>]"
  exit 1
fi


COMPONENT="$1"
shift
ENVIRONMENT="$1"
shift
TERRAFORM_COMMAND="$1"
shift

REGION="us-east-1"
GIT_ROOT="$(git rev-parse --show-toplevel)"
COMPONENT_PATH="$GIT_ROOT/devops/iac/terraform/components/$COMPONENT"
ENVIRONMENT_PATH="$GIT_ROOT/devops/iac/terraform/environments"
COMPONENT_VAR_FILE="$ENVIRONMENT_PATH/$REGION/${COMPONENT}-${ENVIRONMENT}.tfvars"
PROD_LEVEL=${ENVIRONMENT##*-}
BACKEND_VAR_FILE="$ENVIRONMENT_PATH/$REGION/backend.tfvars"
STATE_FILE_S3_KEY="env:/$COMPONENT/$PROD_LEVEL/state.tfstate"
PROFILE_NAME="acf-csfeer"

export AWS_DEFAULT_REGION=$REGION

# Set AWS profile
export AWS_PROFILE=$PROFILE_NAME

echo "Using AWS profile: $PROFILE_NAME"
export AWS_PROFILE="$PROFILE_NAME"

# echo
echo "Logging in to AWS"
aws sts get-caller-identity


# Change to component directory
pushd "$COMPONENT_PATH" > /dev/null
rm -rf .terraform

# Handle init command separately
if echo "$TERRAFORM_COMMAND" | grep -q 'init'; then
  $TERRAFORM_EXECUTABLE init -backend-config="$BACKEND_VAR_FILE" -backend-config="key=$STATE_FILE_S3_KEY" "$@"
  exit_status=$?
else
  # Run Terraform commands with appropriate options
  $TERRAFORM_EXECUTABLE init -backend-config="$BACKEND_VAR_FILE" -backend-config="key=$STATE_FILE_S3_KEY"
  if echo "$TERRAFORM_COMMAND" | grep -Eq 'plan|apply|refresh|destroy|import'; then
    $TERRAFORM_EXECUTABLE "$TERRAFORM_COMMAND" -var-file="$COMPONENT_VAR_FILE" "$@"
  else
    $TERRAFORM_EXECUTABLE "$TERRAFORM_COMMAND" "$@"
  fi
  exit_status=$?
fi

# Change back to original directory
popd > /dev/null

exit $exit_status
