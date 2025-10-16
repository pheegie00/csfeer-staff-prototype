#!/bin/bash

# This script sets up an AWS S3 bucket for storing Terraform state files based on the provided environment and region.

# Usage:
#   ./setup_tf_state_bucket.sh <environment> <region>
# Example:
#   ./setup_tf_state_bucket.sh staging us-west-2

# Parameters:
#   <environment> - The environment for which the S3 bucket is being created (e.g., staging, dev, platform)
#   <region>      - The AWS region where the S3 bucket will be created (e.g., us-west-2)


cd "$(dirname "$0")"
cd ..
ENV=$1
REGION=$2
ENV_DIR="environments/$ENV/$REGION"
PRE_FIX="csfeer"
PROFILE_NAME="acf-csfeer"

export AWS_DEFAULT_REGION=$REGION

# Set AWS profile
export AWS_PROFILE=$PROFILE_NAME

if [ ! -d "$ENV_DIR" ]; then
  cat 1>&2 <<EOF
ERROR: $ENV_DIR not found! Please create the environment dir, if this is your intent.
EOF
  exit 1
fi
LOCATION_ARG=""
if [ "$REGION" != "us-east-1" ]; then
  LOCATION_ARG="--create-bucket-configuration LocationConstraint=$REGION"
fi
BUCKET_NAME="${PRE_FIX}-${ENV}-tf-state-${REGION}"


ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

echo "Press 'return' to create bucket: [$BUCKET_NAME] in account: [$ACCOUNT_ID] region: [$REGION]"
read STUB

aws s3 mb s3://$BUCKET_NAME   --region $REGION $LOCATION_ARG
aws s3api put-bucket-encryption --bucket $BUCKET_NAME --server-side-encryption-configuration '{"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}'
aws s3api put-bucket-versioning --bucket $BUCKET_NAME --versioning-configuration Status=Enabled 
aws s3api put-public-access-block --bucket $BUCKET_NAME --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
