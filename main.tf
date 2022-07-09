resource "aws_vpc" "vps" {
  cidr_block       = "10.1.0.0/16"
  instance_tenancy = "default"

  tags = {
    name      = "vpc"
    terraform = "true"
  }
}