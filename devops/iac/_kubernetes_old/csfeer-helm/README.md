### CSFEER Helm Chart Details

This component manages the deployment of the CSFEER application to Kubernetes via Helm, specifically:

- **Application Configuration**:

  - Deployment of CSFEER
  - Environment-specific configurations:
    - Base values: values.yaml (applied first)
    - Development (dev): values-dev.yaml (overwrites base values)
    - Staging (stage): values-stage.yaml (overwrites base values)
    - Production (prod): values-prod.yaml (overwrites base values)
    - IVV & Perf (dev & stage): optional if you want to overwrite more to point to these locations.

- **Infrastructure Dependencies**:
  - Requires existing which are created by terraform:
    - EKS cluster
    - ArgoCD installation
    - AWS Load Balancer Controller
    - External Secrets Operator

## Setting Up a New Environment

### Prerequisites

Before deploying the CSFEER to a new environment, ensure the following components are set up:

1. **Infrastructure Components**:
   - EKS Cluster
   - ArgoCD Installation
   - AWS Load Balancer Controller
   - External Secrets Operator

### Environment Configuration

1. **Create Environment Values File**:

   ```bash
   # Copy the sample values file
   cp values-sample.yaml values-<environment>.yaml

   # Edit the new values file
   vim values-<environment>.yaml
   ```

2. **Configure Environment Values**:
   - The base `values.yaml` contains common configuration shared across environments
   - In your environment-specific file (e.g., `values-dev.yaml`), you only need to specify values that differ from the base configuration
   - Any values specified in the environment-specific file will override the base values
   - Update environment-specific variables
   - Set environment-specific secrets

### ArgoCD Setup

1. **Login to ArgoCD**:

   ```bash
   # Get ArgoCD admin password from AWS Secrets Manager

   # ARGOCD_PASSWORD_LOCATION is the location of the ArgoCD admin password in AWS Secrets Manager:  "csfeer-staging/argo-cd/admin-password"

   # ARGOCD_APP is the name of the ArgoCD application:  "csfeer-staging"

   ARGOCD_PASSWORD=$(aws secretsmanager get-secret-value \
     --secret-id ${ARGOCD_PASSWORD_LOCATION} \
     --query SecretString \
     --output text \
     --region ${AWS_REGION})

   # Login to ArgoCD
   argocd login "${ARGOCD_HOST}" \
     --username admin \
     --password "${ARGOCD_PASSWORD}" \
     --insecure
   ```

2. **Add Helm Repository**:

   ```bash
   # Add ECR Helm repository to ArgoCD

   # URL is the ECR repository URL:  "FILL IN"

   # CHART_NAME is the name of the Helm chart:  "csfeer"

   # AWS_REGION is the AWS region: "us-east-1"

   argocd repo add "${URL}" \
     --type helm \
     --name "${CHART_NAME}" \
     --enable-oci \
     --username AWS \
     --password "$(aws ecr get-login-password --region ${AWS_REGION})" \
     --upsert
   ```

### Deployment Options

Choose one of the following deployment methods:

#### Option 1: ArgoCD Application (Recommended)

1. Update the `argo-app.yaml`:

   ```yaml
   spec:
     source:
       helm:
         valueFiles:
           - values.yaml # Base values (always applied first)
           - values-<environment>.yaml # Environment-specific overrides
   ```

2. Apply the ArgoCD application:
   ```bash
      argocd app create --file infrastructure/iac/applications-manifests/argo-app.yaml
   ```

### Verification

1. **Check Application Status**:

   ```bash
   # Using ArgoCD
   argocd app get csfeer-api

   # Using kubectl
   kubectl get pods -n csfeer-api
   ```

2. **View Application Logs**:
   ```bash
   kubectl logs -f deployment/csfeer-api -n csfeer-api
   ```

### Troubleshooting

- If ArgoCD sync fails, check:
  - Values file configuration
  - Network connectivity
  - Required secrets existence
- For pod startup issues:
  - Check pod events: `kubectl describe pod -n csfeer-api`
  - Verify resource limits
  - Confirm secrets are properly mounted
