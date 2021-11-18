output "acm_certificate_arn" {
  description = "ACM certificate ARN for the website"
  value       = aws_acm_certificate.main.arn
  sensitive   = false
}