variable "region" {
  default = "eu-central-1"
  type    = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
