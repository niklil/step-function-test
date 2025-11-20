variable "region" { type = string }
variable "tags" { type = map(string) }
variable "ecs_cluster_name" { type = string default = "modernization-demo" }
variable "container_repository_name" { type = string default = "modernization-agent-app" }
