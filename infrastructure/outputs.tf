output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = module.rds.db_instance_endpoint
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = module.rds.db_instance_port
  sensitive   = true
}

output "rds_username" {
  description = "RDS instance root username"
  value       = module.rds.db_instance_username
  sensitive   = true
}

output "rds_password" {
  description = "RDS instance password"
  value       = module.rds.db_instance_password
  sensitive   = true
}