# ECS Cluster (reuse existing or create new)
data "aws_ecs_cluster" "main" {
  cluster_name = "${var.project_name}-${var.environment}"
}

# CloudWatch log group
resource "aws_cloudwatch_log_group" "keycloak" {
  name              = "/ecs/${var.project_name}-keycloak-${var.environment}"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-keycloak-${var.environment}"
  }
}

# IAM role for ECS task execution
resource "aws_iam_role" "keycloak_task_execution" {
  name = "${var.project_name}-keycloak-exec-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "keycloak_task_execution" {
  role       = aws_iam_role.keycloak_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# IAM role for ECS task
resource "aws_iam_role" "keycloak_task" {
  name = "${var.project_name}-keycloak-task-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

# IAM policy for ECS Exec (SSM)
resource "aws_iam_role_policy" "keycloak_task_exec" {
  name = "${var.project_name}-keycloak-exec-policy-${var.environment}"
  role = aws_iam_role.keycloak_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssmmessages:CreateControlChannel",
          "ssmmessages:CreateDataChannel",
          "ssmmessages:OpenControlChannel",
          "ssmmessages:OpenDataChannel"
        ]
        Resource = "*"
      }
    ]
  })
}

# ECS Task Definition
resource "aws_ecs_task_definition" "keycloak" {
  family                   = "${var.project_name}-keycloak-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.keycloak_task_execution.arn
  task_role_arn            = aws_iam_role.keycloak_task.arn

  container_definitions = jsonencode([{
    name      = "keycloak"
    image     = "quay.io/keycloak/keycloak:latest"
    essential = true

    command = ["start-dev"]

    portMappings = [{
      containerPort = 8080
      protocol      = "tcp"
    }]

    environment = [
      { name = "KEYCLOAK_ADMIN", value = var.keycloak_admin_user },
      { name = "KEYCLOAK_ADMIN_PASSWORD", value = var.keycloak_admin_password },
      { name = "KC_DB", value = "postgres" },
      { name = "KC_DB_URL", value = "jdbc:postgresql://${var.db_host}:5432/${var.db_name}" },
      { name = "KC_DB_USERNAME", value = var.db_username },
      { name = "KC_DB_PASSWORD", value = var.db_password },
      { name = "KC_PROXY_HEADERS", value = "xforwarded" },
      { name = "KC_HTTP_ENABLED", value = "true" },
      { name = "KC_HOSTNAME_STRICT", value = "false" },
      { name = "KC_HEALTH_ENABLED", value = "true" },
      { name = "KC_HOSTNAME_STRICT_HTTPS", value = "false" },
      { name = "KC_SPI_REALM_DEFAULT_SSL_REQUIRED", value = "none" },
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.keycloak.name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "keycloak"
      }
    }

    healthCheck = {
      command     = ["CMD-SHELL", "exec 3<>/dev/tcp/localhost/9000 && echo -e 'GET /health/ready HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n' >&3 && cat <&3 | grep -q 'UP'"]
      interval    = 30
      timeout     = 15
      retries     = 5
      startPeriod = 240
    }
  }])

  tags = {
    Name = "${var.project_name}-keycloak-${var.environment}"
  }
}

# ECS Service
resource "aws_ecs_service" "keycloak" {
  name                   = "${var.project_name}-keycloak-${var.environment}"
  cluster                = data.aws_ecs_cluster.main.id
  task_definition        = aws_ecs_task_definition.keycloak.arn
  desired_count          = 1
  launch_type                        = "FARGATE"
  enable_execute_command             = true
  health_check_grace_period_seconds  = 300

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.keycloak.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.keycloak.arn
    container_name   = "keycloak"
    container_port   = 8080
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  depends_on = [aws_lb_listener.keycloak]

  tags = {
    Name = "${var.project_name}-keycloak-${var.environment}"
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}
