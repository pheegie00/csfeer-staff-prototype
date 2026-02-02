# CSFeer ECS Component

This Terraform component deploys the CSFeer Django application to AWS ECS Fargate with Application Load Balancer.

## Architecture

```
Internet → ALB (public subnets) → ECS Fargate Tasks → RDS PostgreSQL
                                        ↓
                                  CloudWatch Logs
```

## Prerequisites

1. VPC with public subnets (for ALB) and private/public subnets (for ECS tasks)
2. RDS database deployed (see `csfeer-rds-simple` component)
3. Docker image pushed to ECR
4. S3 bucket for Terraform state

## Usage

### 1. Deploy RDS First

See `../csfeer-rds-simple/README.md` for RDS deployment.

### 2. Create terraform.tfvars

```bash
cd devops/iac/terraform/components/csfeer-ecs

cat > terraform.tfvars <<EOF
environment         = "dev"
aws_region          = "us-east-1"
vpc_id              = "vpc-xxxxx"
public_subnet_ids   = ["subnet-aaa", "subnet-bbb"]
private_subnet_ids  = ["subnet-xxx", "subnet-yyy"]
ecr_image_uri       = "123456789012.dkr.ecr.us-east-1.amazonaws.com/csfeer:latest"

# From RDS deployment
db_host          = "csfeer-db.xxxxx.us-east-1.rds.amazonaws.com"
db_password      = "your-secure-password"
django_secret_key = "your-django-secret"

# Optional overrides
task_cpu         = "256"    # 0.25 vCPU
task_memory      = "512"    # 0.5 GB
desired_count    = 1
EOF
```

### 3. Initialize and Deploy

```bash
# Initialize Terraform
terraform init \
  -backend-config="bucket=csfeer-terraform-state-YOUR_ACCOUNT_ID" \
  -backend-config="key=dev/csfeer-ecs.tfstate" \
  -backend-config="region=us-east-1"

# Plan
terraform plan

# Apply
terraform apply
```

### 4. Get Application URL

```bash
terraform output alb_url
```

### 5. Run Database Migrations

```bash
# Get task ARN
TASK_ARN=$(aws ecs list-tasks \
  --cluster csfeer-dev \
  --service-name csfeer-dev \
  --query 'taskArns[0]' \
  --output text)

# Connect to container
aws ecs execute-command \
  --cluster csfeer-dev \
  --task $(basename $TASK_ARN) \
  --container csfeer-app \
  --interactive \
  --command "/bin/bash"

# Inside container
cd /app
uv run python manage.py migrate
uv run python manage.py createsuperuser
exit
```

## Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `environment` | Environment name | - | Yes |
| `vpc_id` | VPC ID | - | Yes |
| `public_subnet_ids` | Public subnet IDs for ALB | - | Yes |
| `private_subnet_ids` | Subnet IDs for ECS tasks | - | Yes |
| `ecr_image_uri` | ECR image URI | - | Yes |
| `db_host` | Database host | - | Yes |
| `db_password` | Database password | - | Yes |
| `django_secret_key` | Django SECRET_KEY | - | Yes |
| `task_cpu` | Task CPU units | `"256"` | No |
| `task_memory` | Task memory in MB | `"512"` | No |
| `desired_count` | Number of tasks | `1` | No |
| `enable_execute_command` | Enable ECS Exec | `true` | No |
| `assign_public_ip` | Assign public IP to tasks | `true` | No |

## Outputs

| Output | Description |
|--------|-------------|
| `alb_url` | Application URL |
| `alb_dns_name` | ALB DNS name |
| `ecs_cluster_name` | ECS cluster name |
| `ecs_service_name` | ECS service name |
| `cloudwatch_log_group` | CloudWatch log group name |

## Operations

### View Logs

```bash
aws logs tail /ecs/csfeer-dev --follow
```

### Deploy New Image

```bash
# Push new image to ECR
docker build -t csfeer:latest --target app .
docker tag csfeer:latest YOUR_ECR_URI:latest
docker push YOUR_ECR_URI:latest

# Force new deployment
aws ecs update-service \
  --cluster csfeer-dev \
  --service csfeer-dev \
  --force-new-deployment
```

### Scale Service

```bash
# Update desired_count in terraform.tfvars
desired_count = 3

terraform apply
```

## Cleanup

```bash
terraform destroy
```
