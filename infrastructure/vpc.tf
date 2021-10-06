module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.7.0"

  name = "${local.project}-${var.environment}"
  cidr = "10.0.0.0/16"

  azs              = ["${local.aws_region}a", "${local.aws_region}b", "${local.aws_region}c"]
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets   = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  create_database_subnet_group           = true
  create_database_subnet_route_table     = true
  create_database_internet_gateway_route = true

  enable_dns_hostnames = true
  enable_dns_support   = true
}