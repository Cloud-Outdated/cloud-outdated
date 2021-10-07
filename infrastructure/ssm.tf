resource "aws_kms_key" "parameter_store" {
  description             = "Parameter store KMS master key"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_kms_alias" "parameter_store_alias" {
  name          = "alias/parameter_store_key"
  target_key_id = "${aws_kms_key.parameter_store.id}"
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

resource "aws_ssm_parameter" "postgres-db-name" {
    name        = "/${local.project}/${var.environment}/POSTGRES_DB"
    description = "DB name"
    type        = "SecureString"
    value       = module.rds.db_instance_name
    overwrite   = true
}

resource "aws_ssm_parameter" "postgres-db-host" {
    name        = "/${local.project}/${var.environment}/POSTGRES_HOST"
    description = "DB host"
    type        = "SecureString"
    value       = module.rds.db_instance_endpoint
    overwrite   = true
}

resource "aws_ssm_parameter" "postgres-db-post" {
    name        = "/${local.project}/${var.environment}/POSTGRES_PORT"
    description = "DB port"
    type        = "SecureString"
    value       = module.rds.db_instance_port
    overwrite   = true
}

resource "aws_ssm_parameter" "postgres-db-user" {
    name        = "/${local.project}/${var.environment}/POSTGRES_USER"
    description = "DB user"
    type        = "SecureString"
    value       = module.rds.db_instance_username
    overwrite   = true
}

resource "aws_ssm_parameter" "postgres-db-password" {
    name        = "/${local.project}/${var.environment}/POSTGRES_PASSWORD"
    description = "DB password"
    type        = "SecureString"
    value       = module.rds.db_instance_password
    overwrite   = true
}