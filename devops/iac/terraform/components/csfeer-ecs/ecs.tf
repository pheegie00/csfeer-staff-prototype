# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}"
  }
}

# CloudWatch log group
resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.project_name}-${var.environment}"
  }
}

# ECS Task Definition
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name      = "${var.project_name}-app"
    image     = var.ecr_image_uri
    essential = true

    portMappings = [{
      containerPort = var.container_port
      protocol      = "tcp"
    }]

    environment = [
      { name = "DJANGO_SETTINGS_MODULE", value = "csfeer.settings" },
      { name = "ENVIRONMENT", value = var.environment },
      { name = "DEBUG", value = var.django_debug },
      { name = "DB_CONFIG__PGHOST", value = var.db_host },
      { name = "DB_CONFIG__PGPORT", value = "5432" },
      { name = "DB_CONFIG__PGDATABASE", value = var.db_name },
      { name = "DB_CONFIG__PGUSER", value = var.db_username },
      { name = "DB_CONFIG__PGPASSWORD", value = var.db_password },
      { name = "SECRET_KEY", value = var.django_secret_key },
      { name = "ALLOWED_HOSTS", value = var.allowed_hosts },
      { name = "CSRF_TRUSTED_ORIGINS", value = var.csrf_trusted_origins },
      { name = "USE_OIDC", value = var.use_oidc },
      { name = "OIDC_CONFIG__DOCUMENT_URL", value = var.oidc_document_url },
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.app.name
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }

    healthCheck = {
      command     = ["CMD-SHELL", "curl -f http://localhost:${var.container_port}/health || exit 1"]
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 120  # Increased to allow time for migrations
    }

    linuxParameters = {
      initProcessEnabled = true
    }
  }])

  tags = {
    Name = "${var.project_name}-${var.environment}"
  }
}

# ECS Service
resource "aws_ecs_service" "app" {
  name            = "${var.project_name}-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  enable_execute_command = var.enable_execute_command

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = var.assign_public_ip
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "${var.project_name}-app"
    container_port   = var.container_port
  }

  # Deployment configuration using argument-based syntax
  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100
  
  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  depends_on = [
    aws_lb_listener.http,
    aws_iam_role_policy_attachment.ecs_task_execution
  ]

  tags = {
    Name = "${var.project_name}-${var.environment}"
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}
