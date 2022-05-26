resource "aws_sns_topic" "lambda-alarm-mislav" {
  name = "${local.project}-${var.environment}-lambda-alarm-notification-mislav"
}

resource "aws_sns_topic_subscription" "lambda-alarm-mislav-target" {
  topic_arn = aws_sns_topic.lambda-alarm-mislav.arn
  protocol  = "email"
  endpoint  = "mislav.cimpersak+co@gmail.com"
}

resource "aws_sns_topic" "lambda-alarm-miguel" {
  name = "${local.project}-${var.environment}-lambda-alarm-notification-miguel"
}

resource "aws_sns_topic_subscription" "lambda-alarm-miguel-target" {
  topic_arn = aws_sns_topic.lambda-alarm-miguel.arn
  protocol  = "email"
  endpoint  = "liezun.js+co@gmail.com"
}


module "lambda-invocations-alarm-level-1" {
  source = "terraform-aws-modules/cloudwatch/aws//modules/metric-alarm"

  alarm_name        = "${local.project}-${var.environment}-lambda-invocations-count-level-1"
  alarm_description = "Lambda invocations count within a time frame"

  evaluation_periods  = 5
  period              = 60 # in seconds
  comparison_operator = "GreaterThanOrEqualToThreshold"
  metric_name         = "Invocations"
  namespace           = "AWS/Lambda"
  unit                = "Count"
  threshold           = 50
  statistic           = "Sum"

  alarm_actions = [
    aws_sns_topic.lambda-alarm-mislav.arn,
    aws_sns_topic.lambda-alarm-miguel.arn,
  ]
}

module "lambda-invocations-alarm-level-2" {
  source = "terraform-aws-modules/cloudwatch/aws//modules/metric-alarm"

  alarm_name        = "${local.project}-${var.environment}-lambda-invocations-count-level-2"
  alarm_description = "Lambda invocations count within a time frame"

  evaluation_periods  = 5
  period              = 60 # in seconds
  comparison_operator = "GreaterThanOrEqualToThreshold"
  metric_name         = "Invocations"
  namespace           = "AWS/Lambda"
  unit                = "Count"
  threshold           = 500
  statistic           = "Sum"

  alarm_actions = [
    aws_sns_topic.lambda-alarm-mislav.arn,
    aws_sns_topic.lambda-alarm-miguel.arn,
  ]
}

module "lambda-invocations-alarm-level-3" {
  source = "terraform-aws-modules/cloudwatch/aws//modules/metric-alarm"

  alarm_name        = "${local.project}-${var.environment}-lambda-invocations-count-level-3"
  alarm_description = "Lambda invocations count within a time frame"

  evaluation_periods  = 5
  period              = 60 # in seconds
  comparison_operator = "GreaterThanOrEqualToThreshold"
  metric_name         = "Invocations"
  namespace           = "AWS/Lambda"
  unit                = "Count"
  threshold           = 5000
  statistic           = "Sum"

  alarm_actions = [
    aws_sns_topic.lambda-alarm-mislav.arn,
    aws_sns_topic.lambda-alarm-miguel.arn,
  ]
}
