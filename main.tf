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


module "container_cluster" {
  source = "../modules/compute"

  create_ecs       = true
  ecs_cluster_name = var.ecs_cluster_name
  tags             = var.tags
}

resource "aws_ecr_repository" "app" {
  name                 = var.container_repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = var.tags
}
