output "ecs_cluster_arn" { value = module.container_cluster.ecs_cluster_arn }
output "ecr_repository_url" { value = aws_ecr_repository.app.repository_url }
