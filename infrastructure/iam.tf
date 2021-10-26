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
}

resource "aws_iam_policy" "backend" {
  name   = "cloud-outdated-backend-${var.environment}"
  policy = data.aws_iam_policy_document.backend.json
}

resource "aws_iam_user_policy_attachment" "backend-attach" {
  user       = aws_iam_user.backend.name
  policy_arn = aws_iam_policy.backend.arn
}
