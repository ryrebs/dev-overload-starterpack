terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {

}

# Pull the image
resource "docker_image" "nginx" {
  name         = "nginx"
  keep_locally = false # Don't keep the image after container is built
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id # Image which the container is based on
  name  = var.container_name          # Container name

  ports {
    internal = 80
    external = 8000
  }
}