# CSFeer Infrastructure as Code

Complete AWS ECS Fargate deployment for CSFeer Django application.

## 🚀 Quick Start (START HERE!)

**First time deploying?** → **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** ⭐

This is the **authoritative guide** - follow it exactly for a working deployment on the first try.

**Time:** 45-75 minutes | **Cost:** ~$50/month

### What You Get

✅ **Fully automated setup** - migrations run automatically  
✅ **Intelligent authentication** - adapts to Keycloak availability  
✅ **Health validation** - deployment fails fast if issues  
✅ **Clear instructions** - step-by-step with verification  

---

## 📚 Documentation (2 Files Only!)

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** ⭐ | **Complete deployment guide** | **First deployment - start here!** |
| **[README.md](README.md)** | Overview & navigation | Architecture, costs, quick links |

**All operations via:** `./deploy-dev.sh` script
**Bonus:** SETUP_CHECKLIST.md includes AWS credentials setup in Appendix A

---

## 🔥 One-Command Deploy

```bash
cd terraform
./deploy-dev.sh
# Select: 1 (All - complete setup)
```

---

## 📊 Common Tasks

**View logs:**
```bash
aws logs tail /ecs/csfeer-dev --follow
```

**Check status:**
```bash
cd terraform && ./deploy-dev.sh  
# Select: 6 (Show status)
```

**Deploy new code:**
```bash
cd terraform && ./deploy-dev.sh
# Select: 10 (Rebuild & redeploy)
```

**Teardown everything:**
```bash
cd terraform && ./deploy-dev.sh
# Select: 9 (Teardown)
```

---

## 🏗️ Architecture

```
Internet → ALB → ECS Fargate → RDS PostgreSQL
           ↓
       CloudWatch Logs
```

**Components:**
- Application Load Balancer (ALB): Routes HTTP traffic
- ECS Fargate: Runs Django container (0.25 vCPU, 0.5GB RAM)
- RDS PostgreSQL: Database (db.t3.micro, 20GB storage)
- CloudWatch: Centralized logging

---

## 💰 Cost Breakdown

**Expected monthly cost for dev environment:**
- ECS Fargate: ~$11/month
- RDS db.t3.micro: ~$17/month  
- Application Load Balancer: ~$16/month
- Other (ECR, CloudWatch, data transfer): ~$6/month
- **Total: ~$50/month**

**Save money:**
- Stop RDS when not in use: Saves ~$17/month
- Destroy ECS when not in use: Saves ~$11/month

---

## 🗂️ Directory Structure

```
iac/
├── README.md                      # This file
├── SETUP_CHECKLIST.md             # Complete guide ⭐
│
└── terraform/                     # Infrastructure
    ├── deploy-dev.sh              # Deployment script ⭐
    │
    └── components/                # Terraform modules
        ├── csfeer-ecs/            # ECS Fargate + ALB
        ├── csfeer-rds-simple/     # PostgreSQL RDS
        └── csfeer-keycloak/       # Optional OIDC auth
```

---

## 🆘 Troubleshooting

**Common Issues:**

- **AWS credentials not configured** → [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md#appendix-a-aws-credentials-setup)
- **Task won't start** → Check status: `./deploy-dev.sh` → Option 6
- **Health check failing** → View logs: `aws logs tail /ecs/csfeer-dev --follow`
- **Database connection** → Connect to container: `./deploy-dev.sh` → Option 7

**For all issues:** Use `./deploy-dev.sh` menu options to investigate

---

## 🎯 Technology Stack

### Infrastructure
- **AWS ECS Fargate**: Serverless container orchestration
- **AWS RDS PostgreSQL**: Managed database service
- **Application Load Balancer**: HTTP traffic routing
- **CloudWatch Logs**: Centralized logging
- **ECR**: Private Docker registry
- **Terraform**: Infrastructure as Code

### Application
- **Django 5.x**: Python web framework
- **PostgreSQL 15.8**: Relational database
- **Gunicorn**: WSGI HTTP server
- **Docker**: Containerization

---

## 📋 Next Steps

### Immediate
1. ✅ Read [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
2. ✅ Run `cd terraform && ./deploy-dev.sh`
3. ✅ Bookmark application URL for daily use

### Week 1
- Bookmark application URL
- Set up cost alerts
- Test deploy new code workflow
- Review CloudWatch logs

### Month 1
- Add HTTPS certificate
- Set up CloudWatch alarms
- Test backup/restore
- Review security settings

---

**Ready to deploy?** Start with [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) ⭐
