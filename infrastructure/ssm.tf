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
