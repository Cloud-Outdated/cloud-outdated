resource "aws_route53_zone" "main" {
  name = var.environment != "prod" ? "${var.environment}.${local.project}.com" : "${local.project}.com"
}

# nameservers for prod are set on namecheap.com
# nameservers for dev are set in prod zone

resource "aws_route53_record" "dev_ns" {
  # only in prod workspace
  count = var.environment == "prod" ? 1 : 0
  name = "dev.${local.project}.com"
  ttl             = 60  # TODO increase this to 24 hours: 86400
  type            = "NS"
  zone_id         = aws_route53_zone.main.zone_id

  # NS values from dev zone
  records = [
    "ns-1834.awsdns-37.co.uk.",
    "ns-1304.awsdns-35.org.",
    "ns-779.awsdns-33.net.",
    "ns-304.awsdns-38.com.",
  ]
}

# TODO
# resource "aws_route53_record" "zappa" {
#   name = var.environment != "prod" ? "${var.environment}.${local.project}.com" : "${local.project}.com"
#   ttl             = 60  # TODO increase this to 24 hours: 86400
#   type = "A"
#   zone_id         = aws_route53_zone.main.zone_id
# }

resource "aws_route53_record" "main_certificate_validation" {
  for_each = {
    for dvo in aws_acm_certificate.main.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = aws_route53_zone.main.zone_id
}