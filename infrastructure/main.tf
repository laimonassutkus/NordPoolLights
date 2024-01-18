terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
    external = {
      source  = "hashicorp/external"
      version = "~> 2.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_iam_role" "nord_pool_lights_lambda_function_role" {
  name = "NordPoolLightsLambdaFunctionRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "nord_pool_lights_lambda_function_policy" {
  name        = "NordPoolLightsLambdaFunctionPolicy"
  description = "Policy that allows basic lambda function functionality."
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Action = [
          "ssm:GetParameter"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:ssm:*:*:parameter/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "nord_pool_lights_lambda_function_role_policy_attachment" {
  role       = aws_iam_role.nord_pool_lights_lambda_function_role.name
  policy_arn = aws_iam_policy.nord_pool_lights_lambda_function_policy.arn
}

module "aws_lambda_function" {
  source                    = "terraform-aws-modules/lambda/aws"
  function_name             = "NordPoolLightsFunction"
  lambda_role               = aws_iam_role.nord_pool_lights_lambda_function_role.arn
  create_role               = false
  handler                   = "main.handler"
  timeout                   = 300
  memory_size = 512
  runtime                   = "python3.12"
  source_path               = "${path.module}/../app/"
  build_in_docker           = true
  docker_additional_options = ["--platform=linux/x86_64"]
  environment_variables = {
    COUNTRY = "LT"
    # Electricity price threshold. If current NordPool electricity price exceeds this threshold,
    # the smart plug (indicated by MI_DEVICE_ID) should be turned off. And vice versa.
    PRICE_THRESHOLD = "15"
    # When calculating price, supply your government's applied addition tax (VAT).
    VAT_PERCENTAGE = "21"
    # Smart plug to control according to NordPool electricity price.
    MI_DEVICE_ID = "241011665"
  }
}

resource "aws_ssm_parameter" "nord_pool_lights_mi_account_username" {
  name  = "NordPoolLightsMiAccountUsername"
  type  = "String"
  value = "-"
}

resource "aws_ssm_parameter" "nord_pool_lights_mi_account_password" {
  name  = "NordPoolLightsMiAccountPassword"
  type  = "String"
  value = "-"
}
