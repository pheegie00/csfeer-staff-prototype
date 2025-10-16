<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.11.4 |
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 6.0 |
| <a name="requirement_kubernetes"></a> [kubernetes](#requirement\_kubernetes) | ~> 2.24.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 6.14.1 |
| <a name="provider_kubernetes"></a> [kubernetes](#provider\_kubernetes) | 2.24.0 |
| <a name="provider_terraform"></a> [terraform](#provider\_terraform) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [kubernetes_manifest.argocd_helm_app](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/manifest) | resource |
| [kubernetes_manifest.argocd_helm_keycloak](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/manifest) | resource |
| [kubernetes_manifest.ecr_authorization_token](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/manifest) | resource |
| [kubernetes_manifest.ecr_authorization_token_keycloak](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/manifest) | resource |
| [kubernetes_manifest.ecr_oci_secret](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/manifest) | resource |
| [kubernetes_manifest.ecr_oci_secret_keycloak](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs/resources/manifest) | resource |
| [aws_caller_identity.current](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) | data source |
| [aws_eks_cluster.csfeer_eks_cluster](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/eks_cluster) | data source |
| [aws_iam_openid_connect_provider.csfeer_eks_oidc_provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_openid_connect_provider) | data source |
| [terraform_remote_state.csfeer](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_app_destination"></a> [app\_destination](#input\_app\_destination) | Destination server of the app | `string` | `"https://kubernetes.default.svc"` | no |
| <a name="input_app_helm_chart"></a> [app\_helm\_chart](#input\_app\_helm\_chart) | The Helm chart for the app. ex: 'reloader' | `string` | `"csfeer"` | no |
| <a name="input_app_helm_chart_repo"></a> [app\_helm\_chart\_repo](#input\_app\_helm\_chart\_repo) | Repository containing helm chart - not full path of helm chart. ex: '000.dkr.something.ecr.aws.com/platform/internal/helm/stakater' | `string` | `"FILL IN"` | no |
| <a name="input_app_helm_chart_version"></a> [app\_helm\_chart\_version](#input\_app\_helm\_chart\_version) | Version of the Helm chart to use. ex: '1.2.3' | `string` | n/a | yes |
| <a name="input_app_helm_values_files"></a> [app\_helm\_values\_files](#input\_app\_helm\_values\_files) | App Helm chart values files. | `list(string)` | <pre>[<br>  "values.yaml"<br>]</pre> | no |
| <a name="input_app_name"></a> [app\_name](#input\_app\_name) | Name of the app. Defaults to value of 'app\_helm\_chart' if this is empty/null. | `string` | `""` | no |
| <a name="input_app_namespace"></a> [app\_namespace](#input\_app\_namespace) | Namespace that the app will be deployed to. | `string` | `"null"` | no |
| <a name="input_argocd_app_project"></a> [argocd\_app\_project](#input\_argocd\_app\_project) | Project that this ArgoCD Application belongs to. Useful for tenant restrictions. | `string` | `"default"` | no |
| <a name="input_argocd_namespace"></a> [argocd\_namespace](#input\_argocd\_namespace) | Namespace of ArgoCD. | `string` | `"argocd"` | no |
| <a name="input_aws_ecr_service_account"></a> [aws\_ecr\_service\_account](#input\_aws\_ecr\_service\_account) | ServiceAccount with role for ECR access. Required when chart is in AWS ECR. | `string` | `"argocd-repo-server"` | no |
| <a name="input_aws_region"></a> [aws\_region](#input\_aws\_region) | The AWS region where the infrastructure will be deployed. | `string` | n/a | yes |
| <a name="input_create_namespace"></a> [create\_namespace](#input\_create\_namespace) | Create the namespace with the app rather than separately | `bool` | `false` | no |
| <a name="input_environment_name"></a> [environment\_name](#input\_environment\_name) | The name of the environment where the infrastructure will be deployed. This can be 'dev', 'stage', or 'prod'. | `string` | n/a | yes |
| <a name="input_prune"></a> [prune](#input\_prune) | Prune app: https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/#automatic-pruning | `bool` | `true` | no |
| <a name="input_self_heal"></a> [self\_heal](#input\_self\_heal) | Self-heal app: https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/#automatic-self-healing | `string` | `"False"` | no |
| <a name="input_tf_state_bucket"></a> [tf\_state\_bucket](#input\_tf\_state\_bucket) | The name of the S3 bucket used to store Terraform state files. | `any` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_name"></a> [name](#output\_name) | The name of the csfeer ArgoCD application |
| <a name="output_namespace"></a> [namespace](#output\_namespace) | The namespace of the csfeer ArgoCD application |
| <a name="output_revision"></a> [revision](#output\_revision) | The revision of the csfeer ArgoCD application |
<!-- END_TF_DOCS -->