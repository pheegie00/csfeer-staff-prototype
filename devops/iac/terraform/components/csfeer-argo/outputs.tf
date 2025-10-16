## ---------------------------------------------------------------------------------------------------------------------
## ONE LINE SUMMARY DESCRIBING WHAT IS BEING MANAGED IN THIS SECTION IN ALL CAPS
## The rest of the comments should be in standard casing. This section should contain an overall description of the
## component that is being managed, and highlight any unconventional workarounds or configurations that are in place.
## ---------------------------------------------------------------------------------------------------------------------


output "name" {
  description = "The name of the csfeer ArgoCD application"
  value       = kubernetes_manifest.argocd_helm_app.object.metadata.name
}

output "namespace" {
  description = "The namespace of the csfeer ArgoCD application"
  value       = kubernetes_manifest.argocd_helm_app.object.metadata.namespace
}

output "revision" {
  description = "The revision of the csfeer ArgoCD application"
  value       = kubernetes_manifest.argocd_helm_app.object.spec.source.targetRevision
}