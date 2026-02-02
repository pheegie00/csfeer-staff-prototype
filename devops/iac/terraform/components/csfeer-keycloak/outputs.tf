output "keycloak_url" {
  description = "Keycloak URL"
  value       = "http://${aws_lb.keycloak.dns_name}"
}

output "keycloak_alb_dns" {
  description = "Keycloak ALB DNS name"
  value       = aws_lb.keycloak.dns_name
}

output "keycloak_admin_console" {
  description = "Keycloak admin console URL"
  value       = "http://${aws_lb.keycloak.dns_name}/admin"
}

output "oidc_discovery_url" {
  description = "OIDC discovery URL (after realm is created)"
  value       = "http://${aws_lb.keycloak.dns_name}/realms/csfeer/.well-known/openid-configuration"
}

output "keycloak_security_group_id" {
  description = "Keycloak ECS security group ID"
  value       = aws_security_group.keycloak.id
}
