module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.3.0"

  name        = "${local.project}-${var.environment}"
  description = "${local.project} ${var.environment} security group"
  vpc_id      = module.vpc.vpc_id

  # TODO switch ingress to VPC only
  ingress_with_cidr_blocks = [
    # vpc only ingress
    # {
    #   from_port   = 5432
    #   to_port     = 5432
    #   protocol    = "tcp"
    #   description = "PostgreSQL access from within VPC"
    #   cidr_blocks = module.vpc.vpc_cidr_block
    # },
    # public ingress
    {
      rule        = "postgresql-tcp"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

}