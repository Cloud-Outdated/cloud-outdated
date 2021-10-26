resource "aws_acm_certificate" "main" {
  domain_name = var.environment != "prod" ? "${var.environment}.${local.project}.com" : "${local.project}.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}