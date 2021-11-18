resource "aws_kms_key" "parameter_store" {
  description             = "Parameter store KMS master key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_kms_alias" "parameter_store_alias" {
  name          = "alias/parameter_store_key"
  target_key_id = aws_kms_key.parameter_store.id
}

resource "random_string" "app-secret-key" {
  length  = 50
  upper   = true
  lower   = true
  number  = true
  special = false

  keepers = {
    # Update this to generate new value
    secret_version = "1"
  }
}

resource "aws_ssm_parameter" "app-secret-key" {
  name        = "/${local.project}/${var.environment}/DJANGO_SECRET_KEY"
  description = "SECRET_KEY used by Django setting."
  type        = "SecureString"
  value       = random_string.app-secret-key.result
  overwrite   = true
}

resource "aws_ssm_parameter" "backend-user-access-key-id" {
  name        = "/${local.project}/${var.environment}/AWS_ACCESS_KEY_ID"
  description = "Backend user's AWS_ACCESS_KEY_ID for internal services"
  type        = "SecureString"
  value       = aws_iam_access_key.backend.id
  overwrite   = true
}

resource "aws_ssm_parameter" "backend-user-aws-secret-access-key" {
  name        = "/${local.project}/${var.environment}/AWS_SECRET_ACCESS_KEY"
  description = "Backend user's AWS_SECRET_ACCESS_KEY for internal services"
  type        = "SecureString"
  value       = aws_iam_access_key.backend.secret
  overwrite   = true
}

resource "aws_ssm_parameter" "db-name" {
  name        = "/${local.project}/${var.environment}/DB_NAME"
  description = "DB name"
  type        = "SecureString"
  value       = " "

  # This ^ is manually populated, therefore the lifecycle rule below:
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "db-host" {
  name        = "/${local.project}/${var.environment}/DB_HOST"
  description = "DB host"
  type        = "SecureString"
  value       = " "

  # This ^ is manually populated, therefore the lifecycle rule below:
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "db-port" {
  name        = "/${local.project}/${var.environment}/DB_PORT"
  description = "DB port"
  type        = "SecureString"
  value       = " "

  # This ^ is manually populated, therefore the lifecycle rule below:
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "db-user" {
  name        = "/${local.project}/${var.environment}/DB_USER"
  description = "DB user"
  type        = "SecureString"
  value       = " "

  # This ^ is manually populated, therefore the lifecycle rule below:
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "db-password" {
  name        = "/${local.project}/${var.environment}/DB_PASSWORD"
  description = "DB password"
  type        = "SecureString"
  value       = " "

  # This ^ is manually populated, therefore the lifecycle rule below:
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "backend-user-service-account-key" {
  name        = "/${local.project}/${var.environment}/GCP_SERVICE_ACCOUNT_KEY"
  description = "Backend user's GCP_SERVICE_ACCOUNT_KEY for internal services"
  type        = "SecureString"
  value       = module.service_accounts.key
  overwrite   = true
}
