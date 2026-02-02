# Security group for Keycloak ALB
resource "aws_security_group" "keycloak_alb" {
  name        = "${var.project_name}-keycloak-alb-${var.environment}"
  description = "Security group for Keycloak ALB"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-keycloak-alb-${var.environment}"
  }
}

# Security group for Keycloak ECS tasks
resource "aws_security_group" "keycloak" {
  name        = "${var.project_name}-keycloak-ecs-${var.environment}"
  description = "Security group for Keycloak ECS tasks"
  vpc_id      = var.vpc_id

  ingress {
    description     = "HTTP from ALB"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.keycloak_alb.id]
  }

  ingress {
    description     = "Health check from ALB (management port)"
    from_port       = 9000
    to_port         = 9000
    protocol        = "tcp"
    security_groups = [aws_security_group.keycloak_alb.id]
  }

  # Allow CSFEER app to connect to Keycloak directly (for OIDC discovery)
  ingress {
    description     = "HTTP from CSFEER ECS"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [var.ecs_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-keycloak-ecs-${var.environment}"
  }
}
