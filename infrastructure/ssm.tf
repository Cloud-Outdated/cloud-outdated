resource "aws_kms_key" "parameter_store" {
  description             = "Parameter store KMS master key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_kms_alias" "parameter_store_alias" {
  name          = "alias/parameter_store_key/${var.environment}"
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

resource "aws_ssm_parameter" "deploy-environment" {
  name        = "/${local.project}/${var.environment}/ENVIRONMENT"
  description = "Deploy environment"
  type        = "SecureString"
  value       = var.environment
  overwrite   = true
}

resource "aws_ssm_parameter" "app-secret-key" {
  name        = "/${local.project}/${var.environment}/DJANGO_SECRET_KEY"
  description = "SECRET_KEY used by Django setting."
  type        = "SecureString"
  value       = random_string.app-secret-key.result
  overwrite   = true
}

resource "aws_ssm_parameter" "backend-user-access-key-id" {
  name        = "/${local.project}/${var.environment}/AWS_ACCESS_KEY_ID_BACKEND"
  description = "Backend user's AWS_ACCESS_KEY_ID for internal services"
  type        = "SecureString"
  value       = aws_iam_access_key.backend.id
  overwrite   = true
}

resource "aws_ssm_parameter" "backend-user-aws-secret-access-key" {
  name        = "/${local.project}/${var.environment}/AWS_SECRET_ACCESS_KEY_BACKEND"
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
  name        = "/${local.project}/${var.environment}/GOOGLE_APPLICATION_CREDENTIALS"
  description = "Backend user's GOOGLE_APPLICATION_CREDENTIALS for internal services"
  type        = "SecureString"
  value       = module.service_accounts.key
  overwrite   = true
}


variable "RECAPTCHA_PUBLIC_KEY" {
  type        = string
  description = "RECAPTCHA_PUBLIC_KEY"
}

variable "RECAPTCHA_PRIVATE_KEY" {
  type        = string
  description = "RECAPTCHA_PRIVATE_KEY"
}

resource "aws_ssm_parameter" "backend-recaptcha-v3-public-key" {
  name        = "/${local.project}/${var.environment}/RECAPTCHA_PUBLIC_KEY"
  description = "Backend RECAPTCHA_PUBLIC_KEY for internal services"
  type        = "SecureString"
  value       = var.RECAPTCHA_PUBLIC_KEY
  overwrite   = true
}

resource "aws_ssm_parameter" "backend-recaptcha-v3-private-key" {
  name        = "/${local.project}/${var.environment}/RECAPTCHA_PRIVATE_KEY"
  description = "Backend RECAPTCHA_PRIVATE_KEY for internal services"
  type        = "SecureString"
  value       = var.RECAPTCHA_PRIVATE_KEY
  overwrite   = true
}

resource "aws_ssm_parameter" "new-relic-account-id" {
  name        = "/${local.project}/${var.environment}/NEW_RELIC_ACCOUNT_ID"
  description = "New Relic account id"
  type        = "SecureString"
  value       = "3438061"
  overwrite   = true
}

resource "aws_ssm_parameter" "new-relic-api-key" {
  name        = "/${local.project}/${var.environment}/NEW_RELIC_API_KEY"
  description = "New Relic API key"
  type        = "SecureString"
  value       = ""
  overwrite   = true

  # This ^ is manually populated, therefore the lifecycle rule below:
  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "new-relic-region" {
  name        = "/${local.project}/${var.environment}/NEW_RELIC_REGION"
  description = "New Relic integration region"
  type        = "SecureString"
  value       = "eu"
  overwrite   = true
}

resource "aws_ssm_parameter" "google-analytics-gtag-property-id" {
  name        = "/${local.project}/${var.environment}/GOOGLE_ANALYTICS_GTAG_PROPERTY_ID"
  description = "Google Analytics gtag.js measurement id"
  type        = "SecureString"
  value       = var.environment != "prod" ? "G-F5WFR2V5HX" : "G-M6HH2SF9KK"
  overwrite   = true
}
