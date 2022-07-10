variable "password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "username" {
  description = "Database password"
  type        = string
}

variable "vpc_security_group_ids" {}

variable "allocated_storage" {}

variable "availability_zone" {}

variable "subnet_ids" {}

variable "engine" {}

variable "engine_version" {}

variable "instance_class" {}

variable "multi_az" {}
