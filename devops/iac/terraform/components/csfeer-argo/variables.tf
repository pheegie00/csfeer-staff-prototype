variable "tf_state_bucket" {
  description = "The name of the S3 bucket used to store Terraform state files."
}

variable "aws_region" {
  description = "The AWS region where the infrastructure will be deployed."
  type        = string
}

variable "environment_name" {
  description = "The name of the environment where the infrastructure will be deployed. This can be 'dev', 'stage', or 'prod'."
  type        = string
}
variable "argocd_namespace" {
  description = "Namespace of ArgoCD."
  type        = string
  default     = "argocd"
}

variable "argocd_app_project" {
  description = "Project that this ArgoCD Application belongs to. Useful for tenant restrictions."
  type        = string
  default     = "default"
}

variable "aws_ecr_service_account" {
  description = "ServiceAccount with role for ECR access. Required when chart is in AWS ECR."
  type        = string
  default     = "argocd-repo-server"
}

variable "app_namespace" {
  description = "Namespace that the app will be deployed to."
  type        = string
  default     = "null"
}

variable "create_namespace" {
  description = "Create the namespace with the app rather than separately"
  type        = bool
  default     = false
}

variable "app_name" {
  description = "Name of the app. Defaults to value of 'app_helm_chart' if this is empty/null."
  type        = string
  nullable    = true
  default     = ""
}

variable "app_helm_chart_repo" {
  description = "Repository containing helm chart - not full path of helm chart. ex: '000.dkr.something.ecr.aws.com/platform/internal/helm/stakater'"
  type        = string
  default     = "FILL IN"
}

variable "app_helm_chart" {
  description = "The Helm chart for the app. ex: 'reloader'"
  type        = string
  default     = "csfeer"
}

variable "app_helm_chart_version" {
  description = "Version of the Helm chart to use. ex: '1.2.3'"
  type        = string
}

variable "app_helm_values_files" {
  description = "App Helm chart values files."
  type        = list(string)
  default     = ["values.yaml"]
}

variable "app_destination" {
  description = "Destination server of the app"
  type        = string
  default     = "https://kubernetes.default.svc"
}

variable "self_heal" {
  description = "Self-heal app: https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/#automatic-self-healing"
  type        = string
  default     = "False"
}

variable "prune" {
  description = "Prune app: https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/#automatic-pruning"
  type        = bool
  default     = true
}