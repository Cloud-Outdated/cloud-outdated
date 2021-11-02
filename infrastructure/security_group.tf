module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4.3.0"

  name        = "${local.project}-${var.environment}"
  description = "${local.project} ${var.environment} security group"
  vpc_id      = module.vpc.vpc_id

  ingress_with_cidr_blocks = [
    {
      rule        = "postgresql-tcp"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

  egress_with_cidr_blocks = [
    {
      rule        = "postgresql-tcp"
      cidr_blocks = "0.0.0.0/0"
    },
  ]

}