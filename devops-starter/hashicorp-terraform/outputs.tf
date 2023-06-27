output "container_id" {
  description = "ID of Docker container"
  value       = docker_container.nginx.id
}

output "image_id" {
  description = "ID of Docker image"
  value       = docker_image.nginx.id
}