terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.40"
    }
  }
}

provider "aws" {
  region = var.region
}

module "modernization_lambda" {
  source = "../modules/lambda"

  lambda_functions = {
    handler = {
      source_path  = "../functions/deploy/deploy-artifacts"
      handler      = "lambda_function.lambda_handler"
      runtime      = "python3.11"
      timeout      = 30
      memory_size  = 512
      architecture = "arm64"
    }
  }

  tags = var.tags
}
