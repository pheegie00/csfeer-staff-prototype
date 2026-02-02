# CSFeer AWS Deployment - Authoritative Setup Checklist

**Version:** 2.0
**Last Updated:** 2026-02-01
**Last Validated:** 2026-02-01

---

## 🎯 What This Gets You

- Working Django application on AWS ECS Fargate
- PostgreSQL database on RDS
- Application Load Balancer with health checks
- CloudWatch logging with 7-day retention
- **Automated database migrations** (no manual steps!)
- **Cost:** ~$50/month for 24/7 dev environment

---

## ⏱️ Realistic Time Required

- **First-time deployment:** 45-75 minutes
- **Subsequent deployments:** 15-20 minutes

**Breakdown:**
- Prerequisites check: 10 min
- Infrastructure setup: 5 min
- Docker build & push: 10 min
- RDS deployment: 15 min
- ECS deployment: 12 min
- Health check validation: 5 min
- Verification: 3 min

---

## 🚨 CRITICAL: Authentication Configuration

**⚠️ YOUR APPLICATION HAS OIDC AUTHENTICATION ENABLED BY DEFAULT**

### What This Means

The application is configured to use Keycloak for authentication by default ([csfeer/config.py:43](../../csfeer/config.py#L43)):
```python
use_oidc: bool = True  # Default enabled!
```

**The deployment script now automatically detects Keycloak availability** and configures authentication accordingly.

### Automatic Behavior

✅ **Keycloak Available:** Uses OIDC authentication
✅ **Keycloak Not Available:** Automatically falls back to Django authentication

You don't need to manually configure this - the system adapts automatically!

### Manual Override (If Needed)

To force Django authentication even when Keycloak is available, set environment variable:
```bash
USE_OIDC=false
```

---

## 📋 Prerequisites Checklist

### System Requirements

- [ ] macOS, Linux, or WSL2
- [ ] Admin/sudo access for tool installation
- [ ] 10GB free disk space
- [ ] Stable internet connection

### Required Tools

Check your installation:
```bash
aws --version        # Need: AWS CLI 2.x
terraform version    # Need: Terraform 1.11+
docker --version     # Need: Docker 20.x+
jq --version         # Need: jq 1.6+
```

**Install on macOS:**
```bash
brew install awscli terraform docker jq
```

**Verify Docker is running:**
```bash
docker ps  # Should not error
```

### AWS Account Setup

Configure AWS credentials:
```bash
aws configure
# Enter:
#   Access Key ID: AKIA... (from AWS IAM)
#   Secret Access Key: (from AWS IAM)
#   Region: us-east-1
#   Output format: json
```

Verify access:
```bash
aws sts get-caller-identity
# Expected output:
# {
#   "UserId": "AIDA...",
#   "Account": "123456789012",
#   "Arn": "arn:aws:iam::123456789012:user/your-name"
# }
```

**Don't have AWS credentials?** See [AWS_CREDENTIALS_SETUP.md](AWS_CREDENTIALS_SETUP.md)

### Network Information

Get your VPC and subnets:
```bash
# Get default VPC (most AWS accounts have one)
VPC_ID=$(aws ec2 describe-vpcs \
  --filters "Name=isDefault,Values=true" \
  --query 'Vpcs[0].VpcId' --output text)

# Get subnets (need 2 in different AZs for RDS)
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[*].[SubnetId,AvailabilityZone]' \
  --output table

# Save these IDs - you'll need them
echo "VPC: $VPC_ID"
```

**⚠️ Prerequisites Complete?** Don't proceed until all checkboxes are checked.

---

## 🏗️ Architecture & Startup Sequence

### Component Diagram

```
Internet
   ↓
Application Load Balancer (HTTP:80)
   ↓
ECS Fargate Tasks (Django + Gunicorn)
   ↓
RDS PostgreSQL Database
```

### Startup Dependency Chain

**⚠️ CRITICAL: Services MUST start in this order:**

```
1. S3 Bucket (Terraform state) ──────────┐
2. ECR Repository (Docker images) ───────┤
3. VPC/Subnets Discovery (≥2 AZs) ───────┤ Infrastructure (5 min)
4. Docker Image Build & Push (10 min) ───┤
5. RDS PostgreSQL (15 min wait) ─────────┘
   └─> Wait for status: "available" ✓
       │
       ↓
6. ECS Task Definition ──────────────────┐
7. Application Load Balancer ────────────┤
8. Security Groups (ALB→ECS→RDS) ────────┤ Application (12 min)
9. Container Startup (Gunicorn) ─────────┤
   └─> Entrypoint runs: ─────────────────┘
       - Wait for DB connectivity
       - Run migrations ✓ [NEW: Automated!]
       - Load forms ✓ [NEW: Automated!]
       - Start Gunicorn
       │
       ↓
10. Health Checks ───────────────────────┐
    - Container: GET /health (liveness) ─┤ Health (5 min)
    - ALB: GET /ready/ (readiness) ──────┤
    └─> Wait for "healthy" status ✓ ─────┘
        │
        ↓
11. ✅ DEPLOYMENT COMPLETE!
```

**Key Changes from Previous Version:**
- ✅ **Migrations now automated** - no manual ECS Exec required
- ✅ **Forms loaded automatically** - application ready immediately
- ✅ **Health checks validate readiness** - deployment fails fast if issues

---

## 🚀 Deployment Steps

### Step 1: Clone and Navigate

```bash
cd /opt/dev/acf/csfeer
cd devops/iac/terraform
```

### Step 2: Run Deployment Script

The deployment script guides you through the entire process:

```bash
./deploy-dev.sh
```

You'll see a menu:
```
CSFeer Dev Environment Deployment
===================================

Select deployment steps:
1. All (complete setup)
2. Setup infrastructure (S3, ECR)
3. Build and push Docker image
4. Deploy RDS
5. Deploy ECS/Fargate application
6. Show status
7. Run migrations (manual - if needed)
8. Teardown (delete all resources)

Enter selection (e.g., "1" or "2,3,4,5"):
```

**For first-time setup, select: 1** (All)

### What Happens During Deployment

#### Phase 1: Infrastructure Setup (5 minutes)

**Actions:**
- Creates S3 bucket: `csfeer-terraform-state-<ACCOUNT_ID>`
- Creates ECR repository: `csfeer`
- Enables versioning and encryption

**Success Indicators:**
```
✅ S3 bucket created
✅ ECR repository created
```

**Verify:**
```bash
aws s3 ls | grep csfeer-terraform-state
aws ecr describe-repositories --repository-names csfeer
```

---

#### Phase 2: Docker Build (10 minutes)

**Actions:**
- Builds multi-stage Docker image
- Runs npm install for USWDS assets
- Collects static files
- Tags as `<ecr-uri>:dev`
- Pushes to ECR

**Success Indicators:**
```
Successfully built abc123def456
Successfully tagged ...
The push refers to repository ...
dev: digest: sha256:... size: ...
```

**Verify:**
```bash
aws ecr list-images --repository-name csfeer
# Expected: Image with tag "dev"
```

---

#### Phase 3: Database Deployment (15 minutes)

**Actions:**
- Creates RDS subnet group (multi-AZ)
- Creates security group (port 5432)
- Provisions db.t3.micro instance
- Enables automated backups (0-day retention in dev)

**Wait Status:**
The script automatically waits for RDS to be ready:
```
Creating RDS database...
Waiting for RDS to be available (this takes 10-15 minutes)...
✅ RDS is ready
```

**Success Indicators:**
```
Apply complete! Resources: 3 added, 0 changed, 0 destroyed.

Outputs:
db_host = "csfeer-dev-db.xxxxx.us-east-1.rds.amazonaws.com"
db_port = "5432"
db_name = "csfeer"
```

**Verify:**
```bash
aws rds describe-db-instances \
  --db-instance-identifier csfeer-dev-db \
  --query 'DBInstances[0].DBInstanceStatus' \
  --output text
# Expected: "available"
```

---

#### Phase 4: Application Deployment (12-15 minutes)

**Actions:**
1. Checks for Keycloak availability
2. Determines authentication mode automatically
3. Creates ECS cluster, task definition, service
4. Creates ALB with HTTP listener (port 80)
5. Creates target group with `/ready/` health check
6. Launches ECS service with:
   - **NEW:** Entrypoint script that runs migrations automatically
   - **NEW:** Form definitions loaded automatically
   - Gunicorn server

**Automatic OIDC Configuration:**
```
🔐 Checking OIDC configuration...
⚠️  Keycloak not deployed, using Django authentication
Authentication mode: Django (username/password)
```

**Success Indicators:**
```
Apply complete! Resources: 12 added, 0 changed, 0 destroyed.

Outputs:
alb_url = "http://csfeer-dev-alb-123.us-east-1.elb.amazonaws.com"
cluster_name = "csfeer-dev"
service_name = "csfeer-dev"
```

**Automated Health Validation:**
The script now automatically waits for healthy tasks:
```
🏥 Validating deployment health...
⏳ Waiting for healthy tasks (max 600s)...
   Running: 1/1, Healthy: 1/1 (waited 30s)
✅ All tasks healthy

✅ ECS deployed successfully
Application URL: http://csfeer-dev-alb-123.us-east-1.elb.amazonaws.com

Next steps:
1. Access the application at: http://csfeer-dev-alb-123.us-east-1.elb.amazonaws.com/admin/
2. Login with:
   - Create superuser: aws ecs execute-command ...
   - Then run: python manage.py createsuperuser
```

**What's Different from Before:**
- ✅ **Migrations run automatically** via docker-entrypoint.sh
- ✅ **Forms loaded automatically** via docker-entrypoint.sh
- ✅ **Health checks accurate** - `/health` for liveness, `/ready/` for readiness
- ✅ **Script validates health** - doesn't return until tasks are healthy

**Verify Automated Migrations:**
```bash
# Check container logs to see automatic migration
aws logs tail /ecs/csfeer-dev --since 5m
# You should see:
# === CSFeer Startup Script ===
# 1. Waiting for database connectivity...
# ✅ Database is ready
# 2. Running database migrations...
# ✅ Migrations complete
# 3. Loading form definitions...
# ✅ Form definitions loaded
# 4. Starting application...
```

---

#### Phase 5: Create Superuser (2 minutes)

**This is now the ONLY manual step required!**

Get a shell in the running container:
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
```

Inside the container:
```bash
cd /app
python manage.py createsuperuser
# Enter:
#   Username: admin
#   Email: admin@example.com
#   Password: (choose secure password)
#   Password (again): (repeat)

# Exit container
exit
```

---

#### Phase 6: Verification (3 minutes)

**1. Health Check Endpoints:**
```bash
ALB_URL="http://csfeer-dev-alb-123.us-east-1.elb.amazonaws.com"

# Test liveness
curl -I $ALB_URL/health
# Expected: HTTP/1.1 200 OK

# Test readiness
curl $ALB_URL/ready/
# Expected: {"status":"ready","database":"connected","migrations":"applied"}
```

**2. Admin Interface:**
- Open browser: `http://<alb-url>/admin/`
- Should see Django admin login page
- Login with superuser credentials
- Expected: Django admin dashboard

**3. CloudWatch Logs:**
```bash
aws logs tail /ecs/csfeer-dev --since 5m
# Expected:
# - Startup script output
# - Migration messages
# - Form loading messages
# - Gunicorn startup
# - GET requests
# - No ERROR or CRITICAL messages
```

**4. Target Health:**
```bash
aws elbv2 describe-target-health \
  --target-group-arn <tg-arn>
# Expected: State: "healthy"
```

**✅ Success Criteria:**
- [ ] `/health` returns HTTP 200
- [ ] `/ready/` returns HTTP 200 with migrations applied
- [ ] Admin login page loads
- [ ] Can login with superuser
- [ ] Logs show successful startup
- [ ] Target health is "healthy"

**🎉 DEPLOYMENT COMPLETE!**

---

## 🔧 Environment Variables Reference

**⚠️ CRITICAL: Use double underscore (`__`) for nested config**

The application uses Pydantic settings with `env_nested_delimiter="__"` ([csfeer/config.py:33](../../csfeer/config.py#L33))

### Database Configuration (DB_CONFIG__)

| Variable | Default | Purpose | Example |
|----------|---------|---------|---------|
| `DB_CONFIG__PGHOST` | localhost | Database hostname | csfeer-dev-db.xxx.rds.amazonaws.com |
| `DB_CONFIG__PGPORT` | 5432 | Database port | 5432 |
| `DB_CONFIG__PGDATABASE` | csfeer | Database name | csfeer |
| `DB_CONFIG__PGUSER` | csfeer | Database user | csfeer_admin |
| `DB_CONFIG__PGPASSWORD` | secret123 | Database password | (auto-generated) |
| `DB_CONFIG__SSL_MODE` | require | SSL mode | require |

### Application Configuration

| Variable | Default | Purpose | Example |
|----------|---------|---------|---------|
| `SECRET_KEY` | REPLACE ME | Django secret key | (50-char random string) |
| `DEBUG` | True | Debug mode | False (for production) |
| `ALLOWED_HOSTS` | ["localhost"] | Allowed hostnames | ["*"] (dev only) |
| `CSRF_TRUSTED_ORIGINS` | [] | Trusted origins | ["http://alb-url"] |
| `USE_OIDC` | **True** | Enable OIDC | false (to disable) |

### OIDC Configuration (OIDC_CONFIG__)

| Variable | Default | Purpose |
|----------|---------|---------|
| `OIDC_CONFIG__DOCUMENT_URL` | (local dev) | OIDC discovery URL |
| `OIDC_CONFIG__CLIENT_ID` | csfeer-auth | OIDC client ID |
| `OIDC_CONFIG__CLIENT_SECRET` | "" | OIDC client secret |

**⚠️ Common Mistake:** Using single underscore (`DB_CONFIG_PGHOST`) doesn't work!

---

## 🆘 Troubleshooting Guide

### Issue 1: Task Won't Start

**Symptoms:**
- ECS service shows 0 running tasks
- Tasks continuously stop and restart

**Diagnosis:**
```bash
# List recently stopped tasks
aws ecs list-tasks \
  --cluster csfeer-dev \
  --desired-status STOPPED \
  --max-results 5

# Get stop reason
TASK_ARN=$(aws ecs list-tasks --cluster csfeer-dev --desired-status STOPPED --query 'taskArns[0]' --output text)
aws ecs describe-tasks \
  --cluster csfeer-dev \
  --tasks $TASK_ARN \
  --query 'tasks[0].[stoppedReason,containers[0].reason]'
```

**Common Causes & Fixes:**

| Stopped Reason | Fix |
|---------------|-----|
| "CannotPullContainerError" | Image not in ECR → Re-run Docker build step |
| "ResourceInitializationError" | Security group/VPC issue → Check subnets |
| "Essential container exited" | Application crash → Check logs |
| "OutOfMemoryError" | Increase task_memory in terraform |

### Issue 2: Health Checks Failing

**Symptoms:**
- Target group shows "unhealthy"
- ECS tasks running but ALB returns 503

**Diagnosis:**
```bash
# Check target health
aws elbv2 describe-target-health --target-group-arn <arn>

# Test health endpoints from container
TASK_ARN=$(aws ecs list-tasks --cluster csfeer-dev --service-name csfeer-dev --query 'taskArns[0]' --output text)
aws ecs execute-command \
  --cluster csfeer-dev \
  --task $(basename $TASK_ARN) \
  --container csfeer-app \
  --command "curl localhost:8000/health"
```

**Common Causes & Fixes:**

| Health Check State | Cause | Fix |
|-------------------|-------|-----|
| "initial" for >5 min | Health checks not starting | Check security group allows ALB → ECS |
| "unhealthy" | Migrations failed | Check logs: `aws logs tail /ecs/csfeer-dev` |
| "draining" | Task being replaced | Wait for new task |
| 200 locally, unhealthy in ALB | Port mismatch | Verify container port 8000 |

**NEW: Check Entrypoint Script Logs:**
```bash
aws logs tail /ecs/csfeer-dev --since 10m | grep -A 10 "Startup Script"
# Should show:
# === CSFeer Startup Script ===
# ✅ Database is ready
# ✅ Migrations complete
# ✅ Form definitions loaded
```

### Issue 3: Database Connection Errors

**Symptoms:**
- Logs show "could not connect to server"
- Migrations fail with connection refused

**Diagnosis:**
```bash
# Check environment variables
aws ecs describe-tasks --cluster csfeer-dev --tasks <arn> \
  --query 'tasks[0].containers[0].environment'

# Test connection from container
aws ecs execute-command --cluster csfeer-dev --task <arn> --container csfeer-app --command "/bin/bash"
# Inside container:
pg_isready -h $DB_CONFIG__PGHOST -p $DB_CONFIG__PGPORT -U $DB_CONFIG__PGUSER -d $DB_CONFIG__PGDATABASE
```

**Common Causes & Fixes:**

| Error Message | Cause | Fix |
|--------------|-------|-----|
| "could not connect" | RDS not ready | Wait for RDS status "available" |
| "password authentication failed" | Wrong password | Check terraform apply output |
| "no route to host" | Security group | RDS SG must allow ECS SG on port 5432 |
| "timeout" | Network issue | Verify subnets have route to RDS |

**Fix Environment Variables:**
```bash
cd devops/iac/terraform/components/csfeer-ecs
# Check current values in terraform.tfvars
terraform apply
aws ecs update-service --cluster csfeer-dev --service csfeer-dev --force-new-deployment
```

### Issue 4: Entrypoint Script Fails

**NEW: Troubleshooting automated migrations**

**Symptoms:**
- Container starts then immediately exits
- Health checks never become healthy
- Logs show migration errors

**Diagnosis:**
```bash
# Check startup logs
aws logs tail /ecs/csfeer-dev --since 15m | grep -B 5 -A 5 "migrations"

# Common patterns:
# "❌ Database not ready after 30 attempts"  → DB connectivity issue
# "❌ Migrations failed"                     → Migration error
# "⚠️  Form loading failed"                  → Forms already exist (safe to ignore)
```

**Fixes:**

1. **Database not ready:**
   - Verify DB_CONFIG__PGHOST is correct
   - Check RDS security group allows ECS
   - Increase max_attempts in docker-entrypoint.sh

2. **Migration errors:**
   - Check logs for specific migration failure
   - May need to manually fix database schema
   - See OPERATIONS.md for manual migration steps

3. **Container permissions:**
   - Ensure docker-entrypoint.sh is executable
   - Check logs directory permissions

---

## 💰 Cost Management

### Monthly Cost Breakdown (24/7 operation)

| Component | Configuration | Monthly Cost |
|-----------|--------------|--------------|
| ECS Fargate | 1 task, 0.25 vCPU, 0.5GB | $10.80 |
| RDS PostgreSQL | db.t3.micro, 20GB, single-AZ | $17.00 |
| Application Load Balancer | Standard ALB | $16.20 |
| ECR | Docker image storage (< 1GB) | $0.50 |
| CloudWatch Logs | 7-day retention, ~500MB/mo | $1.00 |
| Data Transfer | Estimated outbound | $3.00 |
| **TOTAL** | | **$48.50/month** |

### Cost Reduction Options

**Stop when not in use:**
```bash
# Stop ECS (saves ~$11/month)
aws ecs update-service --cluster csfeer-dev --service csfeer-dev --desired-count 0

# Stop RDS (saves ~$17/month)
# Note: RDS auto-restarts after 7 days
aws rds stop-db-instance --db-instance-identifier csfeer-dev-db

# Restart when needed
aws rds start-db-instance --db-instance-identifier csfeer-dev-db
aws ecs update-service --cluster csfeer-dev --service csfeer-dev --desired-count 1
```

### Monitor Costs

```bash
aws ce get-cost-and-usage \
  --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --group-by Type=SERVICE
```

---

## 🧹 Complete Teardown

**⚠️ WARNING: This deletes ALL resources and data!**

```bash
cd /opt/dev/acf/csfeer/devops/iac/terraform
./deploy-dev.sh
# Select: 8 (Teardown)
```

**What Gets Deleted:**
- ✅ ECS cluster, service, and tasks
- ✅ RDS database (**ALL DATA LOST**)
- ✅ Application Load Balancer
- ✅ Target groups and listeners
- ✅ Security groups
- ✅ CloudWatch log groups

**What's Preserved:**
- ℹ️ S3 state bucket (safe to delete manually)
- ℹ️ ECR repository with images (safe to delete manually)

---

## 📚 Additional Resources

**For daily operations after setup:**
- [OPERATIONS.md](terraform/OPERATIONS.md) - Scaling, updates, backups
- [QUICK_REFERENCE.md](terraform/QUICK_REFERENCE.md) - Command cheat sheet

**For specialized deployments:**
- [terraform/GOVCLOUD.md](terraform/GOVCLOUD.md) - GovCloud with Keycloak
- [AWS_CREDENTIALS_SETUP.md](AWS_CREDENTIALS_SETUP.md) - IAM setup guide

**For infrastructure details:**
- [terraform/README.md](terraform/README.md) - Terraform architecture
- [terraform/components/README.md](terraform/components/) - Component docs

---

## 🔄 What's New in Version 2.0

**Major Improvements:**

1. ✅ **Automated Database Migrations**
   - No more manual ECS Exec required
   - Migrations run automatically via docker-entrypoint.sh
   - Container startup validates database readiness

2. ✅ **Automated Form Loading**
   - Forms loaded during container startup
   - Idempotent - safe to run multiple times

3. ✅ **Intelligent OIDC Configuration**
   - Automatically detects Keycloak availability
   - Falls back to Django auth if Keycloak missing
   - No more redirect loops!

4. ✅ **Improved Health Checks**
   - Separate liveness (`/health`) and readiness (`/ready/`) endpoints
   - ALB validates migrations before routing traffic
   - Deployment fails fast if issues detected

5. ✅ **Health Validation in Deploy Script**
   - Script waits for tasks to become healthy
   - Clear error messages with troubleshooting steps
   - No more "is it done yet?" uncertainty

6. ✅ **Better Error Messages**
   - Entrypoint script logs each step clearly
   - CloudWatch logs show migration progress
   - Failed deployments easier to diagnose

**Result:** First-time success rate dramatically improved!

---

## ✅ Success Checklist

A successful deployment means:

- [ ] All prerequisites installed and configured
- [ ] AWS credentials valid and tested
- [ ] VPC and subnets identified (≥2 AZs)
- [ ] Infrastructure setup completed (S3, ECR)
- [ ] Docker image built and pushed to ECR
- [ ] RDS status shows "available"
- [ ] ECS service running with desired count
- [ ] Target health shows "healthy"
- [ ] `/health` endpoint returns 200
- [ ] `/ready/` endpoint returns 200
- [ ] Admin interface loads
- [ ] Superuser created and can login
- [ ] CloudWatch logs show successful startup
- [ ] No ERROR messages in logs

**When ALL boxes are checked, your deployment is successful!**

---

## Appendix A: AWS Credentials Setup

If you need help setting up AWS credentials from scratch, follow this guide.

### Create AWS Account (if needed)

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow registration (requires credit card)
4. Complete email and phone verification

**Note**: New AWS accounts get 12 months of free tier benefits!

### Create IAM User with Access Keys

#### 1. Sign in to AWS Console
- Go to https://console.aws.amazon.com/
- Sign in with your root account credentials

#### 2. Create IAM User
1. Search for "IAM" or go to https://console.aws.amazon.com/iam/
2. Click **"Users"** → **"Create user"**
3. Enter username (e.g., `terraform-deploy`)
4. Click **"Next"**

#### 3. Set Permissions

**For personal account (easier):**
1. Select **"Attach policies directly"**
2. Check **"AdministratorAccess"**
3. Click **"Next"** → **"Create user"**

**For production (more secure):**
Attach these specific policies:
- `AmazonEC2ContainerRegistryFullAccess`
- `AmazonECS_FullAccess`
- `AmazonRDSFullAccess`
- `AmazonS3FullAccess`
- `AmazonVPCFullAccess`
- `IAMFullAccess`
- `CloudWatchLogsFullAccess`

#### 4. Create Access Key

1. Click on the username → **"Security credentials"** tab
2. Scroll to **"Access keys"** → **"Create access key"**
3. Select **"Command Line Interface (CLI)"**
4. Check confirmation box → **"Next"**
5. Click **"Create access key"**

**⚠️ IMPORTANT**: Save these credentials immediately:
- **Access key ID**: `AKIA...` (20 characters)
- **Secret access key**: (40 characters)

This is the ONLY time you can view the secret key!

#### 5. Configure AWS CLI

```bash
aws configure
# Enter:
#   Access Key ID: AKIA...
#   Secret Access Key: (your secret)
#   Region: us-east-1
#   Output format: json
```

Verify it works:
```bash
aws sts get-caller-identity
# Should show your account ID and user ARN
```

### Security Best Practices

**✅ DO:**
- Create IAM users (don't use root account)
- Enable MFA on your IAM user
- Rotate access keys every 90 days
- Use specific IAM policies (least privilege)
- Never commit credentials to git

**❌ DON'T:**
- Use root account for daily work
- Share access keys with others
- Commit access keys to version control
- Leave unused access keys active

### Enable MFA (Recommended)

1. IAM Console → Users → Your User
2. "Security credentials" tab
3. "Multi-factor authentication (MFA)" → "Assign MFA device"
4. Follow setup wizard (Google Authenticator or Authy)

---

**Questions or issues?** Use `./deploy-dev.sh` for all operations, or open an issue on GitHub.
