# CSFeer RDS Simple Component

Simple RDS PostgreSQL deployment for development environments.

## Usage

### 1. Create terraform.tfvars

```bash
cd devops/iac/terraform/components/csfeer-rds-simple

cat > terraform.tfvars <<EOF
environment  = "dev"
aws_region   = "us-east-1"
vpc_id       = "vpc-xxxxx"
subnet_ids   = ["subnet-xxx", "subnet-yyy"]

# Generate secure password
db_password  = "$(openssl rand -base64 32)"

# Optional overrides
instance_class      = "db.t3.micro"   # Free tier eligible
allocated_storage   = 20
multi_az           = false            # Single AZ for dev
EOF
```

### 2. Initialize and Deploy

```bash
# Initialize Terraform
terraform init \
  -backend-config="bucket=csfeer-terraform-state-YOUR_ACCOUNT_ID" \
  -backend-config="key=dev/csfeer-rds.tfstate" \
  -backend-config="region=us-east-1"

# Plan
terraform plan

# Apply (takes 10-15 minutes)
terraform apply
```

### 3. Get Database Endpoint

```bash
terraform output db_host
terraform output db_endpoint
```

## Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `environment` | Environment name | - | Yes |
| `vpc_id` | VPC ID | - | Yes |
| `subnet_ids` | Subnet IDs (need 2+) | - | Yes |
| `db_password` | Master password | - | Yes |
| `instance_class` | Instance type | `db.t3.micro` | No |
| `allocated_storage` | Storage in GB | `20` | No |
| `multi_az` | Multi-AZ deployment | `false` | No |

## Outputs

| Output | Description |
|--------|-------------|
| `db_host` | Database host |
| `db_endpoint` | Full endpoint (host:port) |
| `db_name` | Database name |
| `db_username` | Master username |

## Cleanup

```bash
terraform destroy
```

**Note:** By default, no final snapshot is created on destroy (dev environment). For production, set `skip_final_snapshot = false`.
