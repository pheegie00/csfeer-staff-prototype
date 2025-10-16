locals {
  keycloak_app_name            = "keycloak"
  keycloak_ecr_oci_secret_name = "ecr-${local.keycloak_app_name}-helm"
}

resource "kubernetes_manifest" "ecr_authorization_token_keycloak" {
  count = var.aws_ecr_service_account != null ? 1 : 0
  # https://external-secrets.io/latest/api/generator/ecr/
  manifest = {
    apiVersion = "generators.external-secrets.io/v1alpha1"
    kind       = "ECRAuthorizationToken"
    metadata = {
      name      = "ecr-${local.keycloak_app_name}"
      namespace = var.argocd_namespace
    }
    spec = {
      region = var.aws_region
      auth = {
        jwt = {
          serviceAccountRef = {
            name = var.aws_ecr_service_account
          }
        }
      }
    }
  }
}

resource "kubernetes_manifest" "ecr_oci_secret_keycloak" {
  count = var.aws_ecr_service_account != null ? 1 : 0
  manifest = {
    apiVersion = "external-secrets.io/v1"
    kind       = "ExternalSecret"
    metadata = {
      name      = local.keycloak_ecr_oci_secret_name
      namespace = var.argocd_namespace
    }
    spec = {
      refreshInterval = "1h"
      target = {
        name = local.keycloak_ecr_oci_secret_name
        template = {
          metadata = {
            labels = {
              "argocd.argoproj.io/secret-type" = "repository"
            }
          }
          data = {
            name      = local.keycloak_ecr_oci_secret_name
            type      = "helm"
            enableOCI = "true"
            url       = "FILL IN"
            password  = "{{ .password }}"
            username  = "{{ .username }}"
          }
        }
      }
      dataFrom = [
        {
          sourceRef = {
            generatorRef = {
              apiVersion = kubernetes_manifest.ecr_authorization_token_keycloak[0].object.apiVersion
              kind       = kubernetes_manifest.ecr_authorization_token_keycloak[0].object.kind
              name       = kubernetes_manifest.ecr_authorization_token_keycloak[0].object.metadata.name
            }
          }
        }
      ]
    }
  }
}

resource "kubernetes_manifest" "argocd_helm_keycloak" {
  manifest = {
    apiVersion = "argoproj.io/v1alpha1"
    kind       = "Application"
    metadata = {
      name      = local.keycloak_app_name
      namespace = var.argocd_namespace
    }
    spec = {
      project = var.argocd_app_project
      source = {
        chart          = "FILL IN"
        repoURL        = "FILL IN"
        targetRevision = "25.0.1"
        helm = {
          parameters = [
            {
              name  = "global.imageRegistry"
              value = "FILL IN"
            },
            {
              name  = "global.security.allowInsecureImages"
              value = "true"
            },
            {
              name  = "image.registry"
              value = "FILL IN"
            },
            {
              name  = "image.repository"
              value = "FILL IN"
            },
            {
              name  = "postgresql.enabled"
              value = "true"
            },
            {
              name  = "postgresql.image.registry"
              value = "FILL IN"
            },
            {
              name  = "postgresql.image.repository"
              value = "FILL IN"
            },
            {
              name  = "postgresql.image.tag"
              value = "16.6.0-debian-12-r1"
            },
            {
              name  = "postgresql.auth.username"
              value = "bn_keycloak"
            },
            {
              name  = "postgresql.auth.password"
              value = "keycloak-db-password"
            },
            {
              name  = "postgresql.auth.database"
              value = "bitnami_keycloak"
            },
            {
              name  = "postgresql.auth.postgresPassword"
              value = "postgres-admin-password"
            },
            {
              name  = "auth.adminUser"
              value = "admin"
            },
            {
              name  = "auth.adminPassword"
              value = "changeme"
            },
            {
              name  = "production"
              value = "false"
            },
            {
              name  = "ingress.enabled"
              value = "true"
            },
            {
              name  = "ingress.ingressClassName"
              value = "alb"
            },
            {
              name  = "ingress.annotations.alb\\.ingress\\.kubernetes\\.io/scheme"
              value = "internal"
            },
            {
              name  = "ingress.annotations.alb\\.ingress\\.kubernetes\\.io/target-type"
              value = "ip"
            },
            {
              name  = "ingress.annotations.alb\\.ingress\\.kubernetes\\.io/listen-ports"
              value = "[{\"HTTP\": 80}]"
            },
            {
              name  = "ingress.annotations.alb\\.ingress\\.kubernetes\\.io/load-balancer-name"
              value = "keycloak-csfeer-alb"
            },
            {
              name  = "ingress.hostname"
              value = "internal-keycloak-csfeer-alb-993128067.us-east-1.elb.amazonaws.com"
            },
            {
              name  = "ingress.pathType"
              value = "Prefix"
            }

          ]
        }
      }
      destination = {
        server    = var.app_destination
        namespace = "keycloak"
      }
      syncPolicy = {
        syncOptions = [
          "PruneLast=true",
          "PrunePropagationPolicy=foreground",
          "CreateNamespace=true"
        ]
      }
    }
  }
}
