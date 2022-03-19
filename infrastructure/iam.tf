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
  names         = ["${var.environment}-backend"]
  generate_keys = true
  project_roles = [
    "${local.project}=>roles/serviceusage.apiKeysAdmin",
  ]
}

