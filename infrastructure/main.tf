variable "environment" {
  # when using remote exec variable is set in terraform cloud as a terraform
  # var (dev or prod)
  type        = string
  description = "Environment"
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.10.0"
    }
  }

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

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

provider "azuread" {
}

# Create a resource group
resource "azurerm_resource_group" "cloud_outdated" {
  name     = "cloud-outdated"
  location = "Germany West Central"
}

# Retrieve domain information
data "azuread_domains" "current" {
  only_initial = true
}

# Create an application
resource "azuread_application" "cloud_outdated" {
  display_name                   = "${local.project}-${var.environment}"
  fallback_public_client_enabled = true
}


resource "azuread_service_principal" "backend" {
  application_id = azuread_application.cloud_outdated.application_id
}

resource "random_string" "azure_automation_account_password" {
  length  = 16
  upper   = true
  lower   = true
  number  = true
  special = true

  keepers = {
    # Update this to generate new value
    secret_version = "1"
  }
}

resource "azuread_user" "backend" {
  user_principal_name = "${local.project}-backend-${var.environment}@${data.azuread_domains.current.domains.0.domain_name}"
  display_name        = "${local.project}-backend-${var.environment}"
  mail_nickname       = "${local.project}-backend-${var.environment}"
  password            = random_string.azure_automation_account_password.result
}

data "azurerm_client_config" "current" {
}



