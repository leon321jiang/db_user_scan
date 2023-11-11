/*

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
      },
    ],
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_policy"
  description = "IAM policy for logging and DynamoDB access from Lambda"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "dynamodb:GetItem",
          "dynamodb:Scan",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
        ],
        Effect   = "Allow",
        Resource = "*",
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_cloudwatch_event_rule" "lambda_scheduler" {
  name                = "every-5-minutes"
  description         = "Trigger Lambda every 5 minutes"
  schedule_expression = "cron(*/5 * * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.lambda_scheduler.name
  target_id = "lambda_target"
  arn       = aws_lambda_function.scan_db_users.arn
}

resource "aws_lambda_function" "scan_db_users" {
  filename         = "scan_db_users_lambda.zip" # This ZIP file should contain both Python files
  function_name    = "scan_db_users"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "db_user_scanner_lambda.db_user_scanner"
  source_code_hash = filebase64sha256("scan_db_users_lambda.zip")
  runtime          = "python3.8"

  # Attach the IAM role policy to the Lambda function
  depends_on = [aws_iam_role_policy_attachment.lambda_policy_attach]
}


resource "aws_lambda_permission" "allow_cloudwatch_to_call_scan_db_users" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.scan_db_users.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_scheduler.arn
}

*/