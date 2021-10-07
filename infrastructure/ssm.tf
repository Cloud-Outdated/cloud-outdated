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

resource "aws_ssm_parameter" "dummy-value" {
    name        = "/${local.project}/${var.environment}/DUMMY_VALUE"
    description = "dummy value to test dotenv loading"
    type        = "SecureString"
    value       = "foo-bar-baz"
    overwrite   = true
}