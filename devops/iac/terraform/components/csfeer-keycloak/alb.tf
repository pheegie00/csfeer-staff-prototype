# Application Load Balancer for Keycloak
resource "aws_lb" "keycloak" {
  name               = "${var.project_name}-kc-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.keycloak_alb.id]
  subnets            = var.public_subnet_ids

  tags = {
    Name = "${var.project_name}-keycloak-${var.environment}"
  }
}

# Target Group
resource "aws_lb_target_group" "keycloak" {
  name        = "${var.project_name}-kc-${var.environment}"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "9000"
    protocol            = "HTTP"
    timeout             = 10
    unhealthy_threshold = 5
  }

  tags = {
    Name = "${var.project_name}-keycloak-${var.environment}"
  }
}

# HTTP Listener
resource "aws_lb_listener" "keycloak" {
  load_balancer_arn = aws_lb.keycloak.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.keycloak.arn
  }
}
