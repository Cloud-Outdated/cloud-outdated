resource "aws_iam_user" "backend" {
  name = "cloud-outdated-backend-${var.environment}"
}

resource "aws_iam_access_key" "backend" {
  user = aws_iam_user.backend.name
}

data "aws_iam_policy_document" "backend" {
  statement {
    sid    = "SESSendEmail"
    effect = "Allow"

    actions = [
      "ses:SendEmail",
      "ses:SendRawEmail",
      "ses:SendBulkTemplatedEmail",
    ]

    resources = [
      "*",
    ]
  }
  statement {
    sid    = "ServiceVersionPolling"
    effect = "Allow"

    actions = [
      "elasticache:DescribeCacheEngineVersions",
      "es:ListVersions",
      "kafka:ListKafkaVersions",
      "memorydb:DescribeEngineVersions",
      "mq:DescribeBrokerEngineTypes",
      "rds:DescribeDBEngineVersions",
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_policy" "backend" {
  name   = "cloud-outdated-backend-${var.environment}"
  policy = data.aws_iam_policy_document.backend.json
}

resource "aws_iam_user_policy_attachment" "backend-attach" {
  user       = aws_iam_user.backend.name
  policy_arn = aws_iam_policy.backend.arn
}


module "service_accounts" {
  source        = "terraform-google-modules/service-accounts/google"
  version       = "~> 3.0"
  project_id    = local.project
  prefix        = local.project
  names         = ["backend"]
  generate_keys = true
  project_roles = [
    "${local.project}=>roles/serviceusage.apiKeysAdmin",
  ]
}

resource "azurerm_automation_account" "backend" {
  name                = "${local.project}-backend-${var.environment}"
  location            = azurerm_resource_group.cloud_outdated.location
  resource_group_name = azurerm_resource_group.cloud_outdated.name
  sku_name            = "Basic"
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

resource "azurerm_automation_credential" "backend" {
  name                    = "${local.project}-backend-${var.environment}"
  resource_group_name     = azurerm_resource_group.cloud_outdated.name
  automation_account_name = azurerm_automation_account.backend.name
  username                = "${local.project}-backend-${var.environment}"
  password                = random_string.azure_automation_account_password.result
}

data "azurerm_client_config" "current" {
}


