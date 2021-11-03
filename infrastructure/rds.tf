module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 3.4.0"

  identifier = "${local.project}-${var.environment}"

  engine            = "postgres"
  engine_version    = "13.3"
  family            = "postgres13"
  instance_class    = "db.t3.micro"
  allocated_storage = 5

  publicly_accessible = true

  name = "cloudoutdated_${var.environment}"
  username               = "g342n0758b3"
  create_random_password = true
  random_password_length = 20
  port                   = 5432

  maintenance_window              = "Mon:01:00-Mon:04:00"
  backup_window                   = "05:00-08:00"
  backup_retention_period         = 10
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  subnet_ids             = module.vpc.database_subnets
  vpc_security_group_ids = [module.security_group.security_group_id]

  # Database Deletion Protection
  deletion_protection = true

  parameters = [
    {
      name  = "autovacuum"
      value = 1
    },
    {
      name  = "client_encoding"
      value = "utf8"
    }
  ]

  # Enable creation of monitoring IAM role
  create_monitoring_role = true
}
