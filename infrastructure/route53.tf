resource "aws_route53_zone" "main" {
  # TODO if env==prod don't use subdomain
  name = "${var.environment}.${local.project}.com"
}
