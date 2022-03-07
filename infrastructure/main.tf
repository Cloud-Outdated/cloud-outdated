variable "environment" {
  # when using remote exec variable is set in terraform cloud as a terraform
  # var (dev or prod)
  type        = string
  description = "Environment"
}

terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "cloud-outdated"

    workspaces {
      prefix = "co-"
    }
  }
}

provider "aws" {
  # AWS access key and secret are set in terraform cloud as env vars
  region = local.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      Owner       = "terraform"
      Project     = local.project
    }
  }
}

provider "aws" {
  alias  = "virginia"
  region = "us-east-1"
}

provider "google" {
  project = local.project
  region  = local.gcp_region
}
