### S3 Bucket for Load Balancer Logging
resource "aws_s3_bucket" "load_balancer_logging_bucket" {
  bucket              = "${local.name_prefix}-loadbalancer-logging"
  object_lock_enabled = true
}

resource "aws_s3_bucket_versioning" "load_balancer_logging_bucket_versioning" {
  bucket = aws_s3_bucket.load_balancer_logging_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "load_balancer_logging_bucket_lifecycle" {
  bucket     = aws_s3_bucket.load_balancer_logging_bucket.id
  depends_on = [aws_s3_bucket_versioning.load_balancer_logging_bucket_versioning]

  rule {
    id     = "Retire noncurrent object versions"
    status = "Enabled"

    filter {
      prefix = ""
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}

resource "aws_s3_bucket_policy" "load_balancer_logging_bucket_policy" {
  bucket = aws_s3_bucket.load_balancer_logging_bucket.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid       = "RequireSSLOnly",
        Effect    = "Deny",
        Principal = "*",
        Action    = "s3:*",
        Resource = [
          aws_s3_bucket.load_balancer_logging_bucket.arn,
          "${aws_s3_bucket.load_balancer_logging_bucket.arn}/*"
        ],
        Condition = {
          Bool = {
            "aws:SecureTransport" : "false"
          }
        }
      },
      {
        Sid    = "AllowAccessFromELB"
        Action = "s3:PutObject"
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = data.aws_caller_identity.current.account_id
          }
        }
        Effect = "Allow"
        Principal = {
          Service = "logdelivery.elasticloadbalancing.amazonaws.com"
        }
        Resource = "${aws_s3_bucket.load_balancer_logging_bucket.arn}/*"
      },
    ]
  })
}
