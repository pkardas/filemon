resource "aws_vpc" "_" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
}

resource "aws_internet_gateway" "_" {
  vpc_id = aws_vpc._.id
}

resource "aws_route_table" "_" {
  vpc_id = aws_vpc._.id

  dynamic "route" {
    for_each = var.route

    content {
      cidr_block     = route.value.cidr_block
      gateway_id     = route.value.gateway_id
      nat_gateway_id = route.value.nat_gateway_id
    }
  }
}

resource "aws_route_table_association" "_" {
  subnet_id      = var.subnet_id
  route_table_id = aws_route_table._.id
}

