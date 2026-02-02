#!/bin/bash
set -e

# CSFeer Dev Environment Deployment Script
# Deploys RDS and ECS/Fargate to AWS

echo "🚀 CSFeer Dev Environment Deployment"
echo "====================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found${NC}"
    exit 1
fi

if ! command -v terraform &> /dev/null; then
    echo -e "${RED}❌ Terraform not found${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All prerequisites installed${NC}"
echo ""

# OIDC Validation Function
validate_oidc_config() {
    local oidc_url=$1

    if [ -z "$oidc_url" ]; then
        echo -e "${YELLOW}⚠️  OIDC URL is empty${NC}"
        return 1
    fi

    # Test OIDC discovery endpoint accessibility
    if ! curl -sf "$oidc_url" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  OIDC endpoint not accessible: $oidc_url${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ OIDC configuration valid${NC}"
    return 0
}

# Health Check Validation Function
wait_for_healthy_tasks() {
    local cluster=$1
    local service=$2
    local max_wait=600  # 10 minutes
    local waited=0

    echo "⏳ Waiting for healthy tasks (max ${max_wait}s)..."

    while [ $waited -lt $max_wait ]; do
        local running=$(aws ecs describe-services \
            --cluster $cluster \
            --services $service \
            --query 'services[0].runningCount' \
            --output text 2>/dev/null || echo "0")

        local desired=$(aws ecs describe-services \
            --cluster $cluster \
            --services $service \
            --query 'services[0].desiredCount' \
            --output text 2>/dev/null || echo "0")

        if [ "$running" = "$desired" ] && [ "$running" != "0" ]; then
            # Check ALB target health
            cd "${PROJECT_DIR}/devops/iac/terraform/components/csfeer-ecs"
            local target_group_arn=$(terraform output -raw target_group_arn 2>/dev/null || echo "")

            if [ -n "$target_group_arn" ]; then
                local healthy=$(aws elbv2 describe-target-health \
                    --target-group-arn $target_group_arn \
                    --query 'length(TargetHealthDescriptions[?TargetHealth.State==`healthy`])' \
                    --output text 2>/dev/null || echo "0")

                if [ "$healthy" = "$desired" ]; then
                    echo -e "${GREEN}✅ All tasks healthy${NC}"
                    return 0
                fi
                echo "   Running: $running/$desired, Healthy: $healthy/$desired (waited ${waited}s)"
            else
                echo "   Running: $running/$desired (waited ${waited}s)"
            fi
        else
            echo "   Running: $running/$desired (waited ${waited}s)"
        fi

        sleep 10
        waited=$((waited + 10))
    done

    echo -e "${RED}❌ Timeout waiting for healthy tasks${NC}"
    echo -e "${YELLOW}Check logs: aws logs tail /ecs/csfeer-${ENVIRONMENT} --follow${NC}"
    return 1
}

echo ""

# Get AWS account info
echo "🔐 Checking AWS credentials..."
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text 2>/dev/null)
if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo -e "${RED}❌ AWS credentials not configured. Run: aws configure${NC}"
    exit 1
fi

export AWS_USER=$(aws sts get-caller-identity --query Arn --output text 2>/dev/null)
export AWS_REGION=$(aws configure get region)
if [ -z "$AWS_REGION" ]; then
    export AWS_REGION="us-east-1"
    echo -e "${YELLOW}⚠️  No default region set, using us-east-1${NC}"
fi

export ENVIRONMENT="dev"
export PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../" && pwd)"
export TMP_DIR="${PROJECT_DIR}/tmp"

# Ensure tmp directory exists
mkdir -p "${TMP_DIR}"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${BLUE}   AWS Account Configuration${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Account ID: ${NC}${AWS_ACCOUNT_ID}"
echo -e "${GREEN}✅ User/Role:  ${NC}${AWS_USER}"
echo -e "${GREEN}✅ Region:     ${NC}${AWS_REGION}"
echo -e "${GREEN}✅ Environment:${NC} ${ENVIRONMENT}"
echo -e "${BLUE}═══════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}⚠️  This will deploy to YOUR PERSONAL AWS ACCOUNT${NC}"
echo -e "${YELLOW}⚠️  Estimated cost: ~\$45-50/month${NC}"
echo ""
read -p "Continue with this account? [y/N]: " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 0
fi
echo ""

# Main menu
echo "Select action:"
echo "1. Complete setup (all steps)"
echo "2. Setup infrastructure (S3, ECR, VPC info)"
echo "3. Build and push Docker image"
echo "4. Deploy RDS"
echo "5. Deploy ECS/Fargate application"
echo "6. Show application status"
echo "7. Connect to container (shell)"
echo "8. Create superuser & organization (automated)"
echo "9. Teardown (destroy all resources)"
echo "10. Deploy new code (rebuild image + force redeploy)"
read -p "Enter choice [1-10]: " action

case $action in
    1) STEPS="setup docker rds ecs superuser";;
    2) STEPS="setup";;
    3) STEPS="docker";;
    4) STEPS="rds";;
    5) STEPS="ecs";;
    6) STEPS="status";;
    7) STEPS="connect";;
    8) STEPS="superuser";;
    9) STEPS="teardown";;
    10) STEPS="redeploy";;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Function to save environment
save_env() {
    cat > ${TMP_DIR}/csfeer-${ENVIRONMENT}-env.sh <<EOF
export AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID}"
export AWS_REGION="${AWS_REGION}"
export ENVIRONMENT="${ENVIRONMENT}"
export ECR_REPO_URI="${ECR_REPO_URI}"
export VPC_ID="${VPC_ID}"
export SUBNET_IDS="${SUBNET_IDS}"
export DB_PASSWORD="${DB_PASSWORD}"
export DB_HOST="${DB_HOST}"
export DJANGO_SECRET="${DJANGO_SECRET}"
EOF
}

# Load existing environment if available
if [ -f ${TMP_DIR}/csfeer-${ENVIRONMENT}-env.sh ]; then
    source ${TMP_DIR}/csfeer-${ENVIRONMENT}-env.sh
fi

# Setup infrastructure
if [[ $STEPS == *"setup"* ]]; then
    echo ""
    echo "📦 Step 1: Infrastructure Setup"
    echo "==============================="
    
    # Create S3 bucket
    BUCKET_NAME="csfeer-terraform-state-${AWS_ACCOUNT_ID}"
    echo "Creating S3 bucket: $BUCKET_NAME"
    
    if ! aws s3 ls "s3://${BUCKET_NAME}" 2>&1 | grep -q 'NoSuchBucket'; then
        echo -e "${YELLOW}⚠️  Bucket already exists${NC}"
    else
        aws s3 mb "s3://${BUCKET_NAME}" --region ${AWS_REGION}
        
        aws s3api put-bucket-versioning \
            --bucket ${BUCKET_NAME} \
            --versioning-configuration Status=Enabled
        
        aws s3api put-bucket-encryption \
            --bucket ${BUCKET_NAME} \
            --server-side-encryption-configuration \
            '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
        
        aws s3api put-public-access-block \
            --bucket ${BUCKET_NAME} \
            --public-access-block-configuration \
            "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
        
        echo -e "${GREEN}✅ S3 bucket created${NC}"
    fi
    
    # Create ECR repository
    echo ""
    echo "Creating ECR repository..."
    if ! aws ecr describe-repositories --repository-names csfeer --region ${AWS_REGION} &> /dev/null; then
        aws ecr create-repository --repository-name csfeer --region ${AWS_REGION}
        echo -e "${GREEN}✅ ECR repository created${NC}"
    else
        echo -e "${YELLOW}⚠️  ECR repository already exists${NC}"
    fi
    
    export ECR_REPO_URI=$(aws ecr describe-repositories \
        --repository-names csfeer \
        --query 'repositories[0].repositoryUri' \
        --output text)
    echo -e "${GREEN}✅ ECR URI: ${ECR_REPO_URI}${NC}"
    
    # Get VPC information
    echo ""
    echo "Getting VPC information..."
    export VPC_ID=$(aws ec2 describe-vpcs \
        --filters "Name=is-default,Values=true" \
        --query 'Vpcs[0].VpcId' \
        --output text)
    
    if [ "$VPC_ID" = "None" ] || [ -z "$VPC_ID" ]; then
        echo -e "${RED}❌ No default VPC found${NC}"
        read -p "Enter VPC ID: " VPC_ID
    fi
    
    echo -e "${GREEN}✅ VPC ID: ${VPC_ID}${NC}"
    
    # Get subnet IDs
    export SUBNET_IDS=$(aws ec2 describe-subnets \
        --filters "Name=vpc-id,Values=${VPC_ID}" \
        --query 'Subnets[0:2].SubnetId' \
        --output text | tr '\t' ',')
    
    echo -e "${GREEN}✅ Subnets: ${SUBNET_IDS}${NC}"
    
    save_env
    echo ""
    echo -e "${GREEN}✅ Infrastructure setup complete${NC}"
fi

# Build and push Docker image
if [[ $STEPS == *"docker"* ]]; then
    echo ""
    echo "🐳 Step 2: Build and Push Docker Image"
    echo "======================================="
    
    cd ${PROJECT_DIR}
    
    echo "Building Docker image for linux/amd64 (AWS Fargate)..."
    docker build --platform linux/amd64 -t csfeer:latest --target app .
    
    echo "Logging in to ECR..."
    aws ecr get-login-password --region ${AWS_REGION} | \
        docker login --username AWS --password-stdin \
        ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
    
    echo "Tagging image..."
    docker tag csfeer:latest ${ECR_REPO_URI}:latest
    docker tag csfeer:latest ${ECR_REPO_URI}:${ENVIRONMENT}
    
    echo "Pushing image..."
    docker push ${ECR_REPO_URI}:latest
    docker push ${ECR_REPO_URI}:${ENVIRONMENT}
    
    save_env
    echo ""
    echo -e "${GREEN}✅ Docker image pushed${NC}"
fi

# Deploy RDS
if [[ $STEPS == *"rds"* ]]; then
    echo ""
    echo "🗄️  Step 3: Deploy RDS"
    echo "====================="
    
    cd ${PROJECT_DIR}/devops/iac/terraform/components/csfeer-rds-simple
    
    # Generate password if not exists
    if [ -z "$DB_PASSWORD" ]; then
        # Generate password without forbidden characters (/, @, ", space)
        export DB_PASSWORD=$(openssl rand -base64 32 | tr -d '/@ "')
        echo -e "${YELLOW}⚠️  Generated database password${NC}"
        echo -e "${YELLOW}Password: ${DB_PASSWORD}${NC}"
        echo -e "${YELLOW}⚠️  SAVE THIS PASSWORD!${NC}"
    fi
    
    # Initialize Terraform
    echo ""
    echo "Initializing Terraform..."
    terraform init \
        -backend-config="bucket=csfeer-terraform-state-${AWS_ACCOUNT_ID}" \
        -backend-config="key=${ENVIRONMENT}/csfeer-rds.tfstate" \
        -backend-config="region=${AWS_REGION}"
    
    # Deploy
    echo ""
    echo "Deploying RDS (this takes 10-15 minutes)..."
    terraform apply -auto-approve \
        -var="environment=${ENVIRONMENT}" \
        -var="aws_region=${AWS_REGION}" \
        -var="vpc_id=${VPC_ID}" \
        -var="subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
        -var="db_password=${DB_PASSWORD}"
    
    export DB_HOST=$(terraform output -raw db_host)
    
    save_env
    echo ""
    echo -e "${GREEN}✅ RDS deployed${NC}"
    echo -e "${GREEN}Database host: ${DB_HOST}${NC}"
fi

# Deploy ECS
if [[ $STEPS == *"ecs"* ]]; then
    echo ""
    echo "🐳 Step 4: Deploy ECS/Fargate"
    echo "============================="
    
    cd ${PROJECT_DIR}/devops/iac/terraform/components/csfeer-ecs
    
    # Generate Django secret if not exists
    if [ -z "$DJANGO_SECRET" ]; then
        export DJANGO_SECRET=$(openssl rand -base64 50)
        echo -e "${YELLOW}⚠️  Generated Django secret key${NC}"
    fi
    
    # Initialize Terraform
    echo ""
    echo "Initializing Terraform..."
    terraform init \
        -backend-config="bucket=csfeer-terraform-state-${AWS_ACCOUNT_ID}" \
        -backend-config="key=${ENVIRONMENT}/csfeer-ecs.tfstate" \
        -backend-config="region=${AWS_REGION}"
    
    # Get Keycloak URL if available and validate OIDC configuration
    KEYCLOAK_URL=""
    USE_OIDC="false"
    OIDC_DOCUMENT_URL=""

    echo ""
    echo "🔐 Checking OIDC configuration..."

    if aws elbv2 describe-load-balancers --names csfeer-keycloak-dev 2>/dev/null; then
        KEYCLOAK_URL=$(aws elbv2 describe-load-balancers \
            --names csfeer-keycloak-dev \
            --query 'LoadBalancers[0].DNSName' \
            --output text 2>/dev/null || echo "")

        if [ -n "$KEYCLOAK_URL" ]; then
            KEYCLOAK_URL="http://${KEYCLOAK_URL}"
            OIDC_DOCUMENT_URL="${KEYCLOAK_URL}/realms/csfeer/.well-known/openid-configuration"

            if validate_oidc_config "$OIDC_DOCUMENT_URL"; then
                USE_OIDC="true"
                echo -e "${GREEN}✅ OIDC authentication will be enabled${NC}"
                echo -e "${BLUE}   Keycloak URL: ${KEYCLOAK_URL}${NC}"
            else
                echo -e "${YELLOW}⚠️  Keycloak not ready, deploying with Django authentication${NC}"
            fi
        else
            echo -e "${YELLOW}⚠️  Keycloak load balancer found but no DNS name${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  Keycloak not deployed, using Django authentication${NC}"
    fi

    echo -e "${BLUE}Authentication mode: $([ "$USE_OIDC" = "true" ] && echo "OIDC (Keycloak)" || echo "Django (username/password)")${NC}"

    # Deploy
    echo ""
    echo "Deploying ECS (this takes 5-10 minutes)..."
    terraform apply -auto-approve \
        -var="environment=${ENVIRONMENT}" \
        -var="aws_region=${AWS_REGION}" \
        -var="vpc_id=${VPC_ID}" \
        -var="public_subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
        -var="private_subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
        -var="ecr_image_uri=${ECR_REPO_URI}:${ENVIRONMENT}" \
        -var="db_host=${DB_HOST}" \
        -var="db_password=${DB_PASSWORD}" \
        -var="django_secret_key=${DJANGO_SECRET}" \
        -var="use_oidc=${USE_OIDC}" \
        -var="oidc_document_url=${OIDC_DOCUMENT_URL}"

    export APP_URL=$(terraform output -raw alb_url)

    # Update with CSRF_TRUSTED_ORIGINS now that we know the ALB URL
    echo ""
    echo "Updating with CSRF_TRUSTED_ORIGINS..."
    terraform apply -auto-approve \
        -var="environment=${ENVIRONMENT}" \
        -var="aws_region=${AWS_REGION}" \
        -var="vpc_id=${VPC_ID}" \
        -var="public_subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
        -var="private_subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
        -var="ecr_image_uri=${ECR_REPO_URI}:${ENVIRONMENT}" \
        -var="db_host=${DB_HOST}" \
        -var="db_password=${DB_PASSWORD}" \
        -var="django_secret_key=${DJANGO_SECRET}" \
        -var="use_oidc=${USE_OIDC}" \
        -var="oidc_document_url=${OIDC_DOCUMENT_URL}" \
        -var="csrf_trusted_origins=[\"http://${APP_URL}\"]"

    save_env

    # Wait for healthy tasks
    echo ""
    echo "🏥 Validating deployment health..."
    if wait_for_healthy_tasks "csfeer-${ENVIRONMENT}" "csfeer-${ENVIRONMENT}"; then
        echo ""
        echo -e "${GREEN}✅ ECS deployed successfully${NC}"
        echo -e "${GREEN}Application URL: http://${APP_URL}${NC}"
        echo ""
        echo -e "${BLUE}Next steps:${NC}"
        echo "1. Access the application at: http://${APP_URL}/admin/"
        echo "2. Create superuser: ./deploy-dev.sh → Option 8"
    else
        echo ""
        echo -e "${RED}❌ Deployment completed but tasks are not healthy${NC}"
        echo -e "${YELLOW}Troubleshooting:${NC}"
        echo "- Check status: ./deploy-dev.sh → Option 6"
        echo "- View logs: aws logs tail /ecs/csfeer-${ENVIRONMENT} --follow"
        echo "- Connect to container: ./deploy-dev.sh → Option 7"
        exit 1
    fi
fi

# Show status
if [[ $STEPS == *"status"* ]]; then
    echo ""
    echo "📊 Application Status"
    echo "===================="
    
    if [ -n "$APP_URL" ]; then
        echo -e "${BLUE}Application URL: ${APP_URL}${NC}"
    fi
    
    echo ""
    echo "ECS Service:"
    aws ecs describe-services \
        --cluster csfeer-${ENVIRONMENT} \
        --services csfeer-${ENVIRONMENT} \
        --query 'services[0].[serviceName,status,runningCount,desiredCount]' \
        --output table
    
    echo ""
    echo "Running Tasks:"
    aws ecs list-tasks \
        --cluster csfeer-${ENVIRONMENT} \
        --service-name csfeer-${ENVIRONMENT}
    
    echo ""
    echo "RDS Status:"
    aws rds describe-db-instances \
        --db-instance-identifier csfeer-${ENVIRONMENT}-db \
        --query 'DBInstances[0].[DBInstanceIdentifier,DBInstanceStatus,Endpoint.Address]' \
        --output table
    
    echo ""
    echo "View logs with:"
    echo "  aws logs tail /ecs/csfeer-${ENVIRONMENT} --follow"
fi

# Connect to container
if [[ $STEPS == *"connect"* ]]; then
    echo ""
    echo "🔄 Connect to Container (Migrations/Superuser)"
    echo "=============================================="

    echo "Finding running task..."
    TASK_ARN=$(aws ecs list-tasks \
        --cluster csfeer-${ENVIRONMENT} \
        --service-name csfeer-${ENVIRONMENT} \
        --desired-status RUNNING \
        --query 'taskArns[0]' \
        --output text)

    if [ -z "$TASK_ARN" ] || [ "$TASK_ARN" = "None" ]; then
        echo -e "${RED}❌ No running tasks found${NC}"
        echo "Run deployment first: ./deploy-dev.sh → Option 1 or 5"
        exit 1
    fi

    TASK_ID=$(basename $TASK_ARN)
    echo -e "${GREEN}✅ Found task: ${TASK_ID}${NC}"

    # Wait for task and execute command agent to be ready
    echo "Checking task readiness..."
    MAX_WAIT=60
    WAITED=0

    while [ $WAITED -lt $MAX_WAIT ]; do
        TASK_STATUS=$(aws ecs describe-tasks \
            --cluster csfeer-${ENVIRONMENT} \
            --tasks $TASK_ARN \
            --query 'tasks[0].lastStatus' \
            --output text)

        AGENT_STATUS=$(aws ecs describe-tasks \
            --cluster csfeer-${ENVIRONMENT} \
            --tasks $TASK_ARN \
            --query 'tasks[0].containers[0].managedAgents[0].lastStatus' \
            --output text 2>/dev/null || echo "PENDING")

        if [ "$TASK_STATUS" = "RUNNING" ] && [ "$AGENT_STATUS" = "RUNNING" ]; then
            echo -e "${GREEN}✅ Task is ready!${NC}"
            break
        fi

        echo "   Task: $TASK_STATUS, Execute Agent: $AGENT_STATUS (waited ${WAITED}s)"
        sleep 5
        WAITED=$((WAITED + 5))
    done

    if [ $WAITED -ge $MAX_WAIT ]; then
        echo -e "${RED}❌ Task not ready after ${MAX_WAIT}s${NC}"
        exit 1
    fi

    echo ""
    echo -e "${BLUE}Connecting to container...${NC}"
    echo ""
    echo "Inside the container, you can run:"
    echo "  cd /app"
    echo "  python manage.py migrate          # Run migrations"
    echo "  python manage.py createsuperuser  # Create admin user"
    echo "  python manage.py shell            # Django shell"
    echo "  exit                              # Exit container"
    echo ""

    aws ecs execute-command \
        --cluster csfeer-${ENVIRONMENT} \
        --task $TASK_ID \
        --container csfeer-app \
        --interactive \
        --command "/bin/bash"
fi

# Create superuser (automated)
if [[ $STEPS == *"superuser"* ]]; then
    echo ""
    echo "👤 Create Django Superuser & Organization"
    echo "=========================================="

    # Get superuser details
    read -p "Username [admin]: " SUPERUSER_USERNAME
    SUPERUSER_USERNAME=${SUPERUSER_USERNAME:-admin}

    read -p "Email [admin@example.com]: " SUPERUSER_EMAIL
    SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-admin@example.com}

    read -sp "Password: " SUPERUSER_PASSWORD
    echo ""

    if [ -z "$SUPERUSER_PASSWORD" ]; then
        echo -e "${RED}❌ Password cannot be empty${NC}"
        exit 1
    fi

    # Get organization details
    read -p "Organization Name [Demo Organization]: " ORG_NAME
    ORG_NAME=${ORG_NAME:-Demo Organization}

    echo ""
    echo "Finding running task..."
    TASK_ARN=$(aws ecs list-tasks \
        --cluster csfeer-${ENVIRONMENT} \
        --service-name csfeer-${ENVIRONMENT} \
        --desired-status RUNNING \
        --query 'taskArns[0]' \
        --output text)

    if [ -z "$TASK_ARN" ] || [ "$TASK_ARN" = "None" ]; then
        echo -e "${RED}❌ No running tasks found${NC}"
        exit 1
    fi

    TASK_ID=$(basename $TASK_ARN)
    echo -e "${GREEN}✅ Found task${NC}"

    # Wait for task to be ready
    echo "Waiting for task readiness..."
    sleep 10

    # Create superuser using interactive mode (ECS requirement)
    echo "Creating superuser..."
    aws ecs execute-command \
        --cluster csfeer-${ENVIRONMENT} \
        --task $TASK_ID \
        --container csfeer-app \
        --interactive \
        --command "/bin/bash -c 'cd /app && export DJANGO_SUPERUSER_USERNAME=\"${SUPERUSER_USERNAME}\" && export DJANGO_SUPERUSER_EMAIL=\"${SUPERUSER_EMAIL}\" && export DJANGO_SUPERUSER_PASSWORD=\"${SUPERUSER_PASSWORD}\" && python manage.py createsuperuser --noinput'" \
        --region us-east-1

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Superuser created successfully!${NC}"

        # Create organization and link user
        echo ""
        echo "Setting up organization and user membership..."

        # Use --all flag to seed org for all users (avoids email lookup issues)
        SEED_CMD=$(printf 'cd /app && python manage.py seed_demo_org --all --org-name "%s"' "${ORG_NAME}")

        aws ecs execute-command \
            --cluster csfeer-${ENVIRONMENT} \
            --task $TASK_ID \
            --container csfeer-app \
            --interactive \
            --command "/bin/bash -c \"${SEED_CMD}\"" \
            --region us-east-1

        echo ""
        echo -e "${YELLOW}Please check the output above for success message.${NC}"
        echo -e "${YELLOW}If the seed command failed, you can run it manually via option 7:${NC}"
        echo -e "${YELLOW}  python manage.py seed_demo_org --all --org-name \"${ORG_NAME}\"${NC}"

        echo ""
        echo "Login credentials:"
        echo "  Username: ${SUPERUSER_USERNAME}"
        echo "  Email: ${SUPERUSER_EMAIL}"
        echo "  Password: (the one you entered)"
        echo "  Organization: ${ORG_NAME}"
        echo ""
        echo "Access admin at: ${APP_URL}/admin/"
    else
        echo -e "${YELLOW}⚠️  Superuser may already exist or creation failed${NC}"
        echo "Try option 7 (Connect to container) to create manually"
    fi
fi

# Redeploy (rebuild image + force new deployment)
if [[ $STEPS == *"redeploy"* ]]; then
    echo ""
    echo "🚀 Deploy New Code"
    echo "=================="

    # Step 1: Rebuild Docker image
    cd ${PROJECT_DIR}

    echo "Building Docker image for linux/amd64 (AWS Fargate)..."
    docker build --platform linux/amd64 -t csfeer:latest --target app .

    echo "Logging in to ECR..."
    aws ecr get-login-password --region ${AWS_REGION} | \
        docker login --username AWS --password-stdin \
        ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

    echo "Tagging image..."
    docker tag csfeer:latest ${ECR_REPO_URI}:latest
    docker tag csfeer:latest ${ECR_REPO_URI}:${ENVIRONMENT}

    echo "Pushing image..."
    docker push ${ECR_REPO_URI}:latest
    docker push ${ECR_REPO_URI}:${ENVIRONMENT}

    echo -e "${GREEN}✅ Docker image pushed${NC}"

    # Step 2: Force new ECS deployment
    echo ""
    echo "Forcing new ECS deployment..."
    aws ecs update-service \
        --cluster csfeer-${ENVIRONMENT} \
        --service csfeer-${ENVIRONMENT} \
        --force-new-deployment \
        --no-cli-pager

    echo -e "${GREEN}✅ Deployment initiated${NC}"

    # Step 3: Wait for deployment
    echo ""
    echo "⏳ Waiting for new tasks to start (this takes 2-3 minutes)..."
    sleep 120

    # Step 4: Check status
    echo ""
    echo "📊 Deployment Status:"
    aws ecs describe-services \
        --cluster csfeer-${ENVIRONMENT} \
        --services csfeer-${ENVIRONMENT} \
        --query 'services[0].[serviceName,status,runningCount,desiredCount]' \
        --output table

    echo ""
    echo -e "${GREEN}✅ Code deployment complete!${NC}"
    echo -e "${BLUE}Check logs: aws logs tail /ecs/csfeer-${ENVIRONMENT} --follow${NC}"
    echo -e "${BLUE}Application URL: ${APP_URL}${NC}"
fi

# Teardown
if [[ $STEPS == *"teardown"* ]]; then
    echo ""
    echo "🗑️  Teardown"
    echo "==========="
    
    # Destroy ECS
    if [ -d "${PROJECT_DIR}/devops/iac/terraform/components/csfeer-ecs" ]; then
        echo ""
        echo "Destroying ECS..."
        cd ${PROJECT_DIR}/devops/iac/terraform/components/csfeer-ecs

        if [ -f terraform.tfstate ] || [ -f .terraform/terraform.tfstate ]; then
            terraform destroy -auto-approve \
                -var="environment=${ENVIRONMENT}" \
                -var="aws_region=${AWS_REGION}" \
                -var="vpc_id=${VPC_ID}" \
                -var="public_subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
                -var="private_subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
                -var="ecr_image_uri=${ECR_REPO_URI}:${ENVIRONMENT}" \
                -var="db_host=${DB_HOST}" \
                -var="db_password=${DB_PASSWORD}" \
                -var="django_secret_key=${DJANGO_SECRET}"

            echo -e "${GREEN}✅ ECS destroyed${NC}"
        fi
    fi

    # Destroy Keycloak
    if [ -d "${PROJECT_DIR}/devops/iac/terraform/components/csfeer-keycloak" ]; then
        echo ""
        echo "Destroying Keycloak..."
        cd ${PROJECT_DIR}/devops/iac/terraform/components/csfeer-keycloak

        if [ -f terraform.tfstate ] || [ -f .terraform/terraform.tfstate ]; then
            # Load Keycloak DB config if available
            KC_DB_HOST="${KC_DB_HOST:-placeholder}"
            KC_DB_PASSWORD="${KC_DB_PASSWORD:-placeholder}"

            terraform destroy -auto-approve \
                -var="environment=${ENVIRONMENT}" \
                -var="aws_region=${AWS_REGION}" \
                -var="vpc_id=${VPC_ID}" \
                -var="public_subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
                -var="private_subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
                -var="db_host=${KC_DB_HOST}" \
                -var="db_name=keycloak" \
                -var="db_username=keycloak_admin" \
                -var="db_password=${KC_DB_PASSWORD}"

            echo -e "${GREEN}✅ Keycloak destroyed${NC}"
        fi
    fi
    
    # Destroy RDS
    if [ -d "${PROJECT_DIR}/devops/iac/terraform/components/csfeer-rds-simple" ]; then
        echo ""
        echo "Destroying RDS..."
        cd ${PROJECT_DIR}/devops/iac/terraform/components/csfeer-rds-simple
        
        if [ -f terraform.tfstate ] || [ -f .terraform/terraform.tfstate ]; then
            terraform destroy -auto-approve \
                -var="environment=${ENVIRONMENT}" \
                -var="aws_region=${AWS_REGION}" \
                -var="vpc_id=${VPC_ID}" \
                -var="subnet_ids=[\"$(echo $SUBNET_IDS | sed 's/,/","/g')\"]" \
                -var="db_password=${DB_PASSWORD}"
            
            echo -e "${GREEN}✅ RDS destroyed${NC}"
        fi
    fi
    
    # Clean up environment file
    rm -f ${TMP_DIR}/csfeer-${ENVIRONMENT}-env.sh
    
    echo ""
    echo -e "${GREEN}✅ Teardown complete${NC}"
    echo -e "${YELLOW}Note: ECR and S3 state bucket still exist${NC}"
fi

echo ""
echo "================================"
echo -e "${GREEN}🎉 Done!${NC}"

if [ -f ${TMP_DIR}/csfeer-${ENVIRONMENT}-env.sh ]; then
    echo ""
    echo "Environment saved to: ${TMP_DIR}/csfeer-${ENVIRONMENT}-env.sh"
    echo "Load it with: source ${TMP_DIR}/csfeer-${ENVIRONMENT}-env.sh"
fi

if [ -n "$APP_URL" ]; then
    echo ""
    echo -e "${BLUE}Application URL: ${APP_URL}${NC}"
fi
