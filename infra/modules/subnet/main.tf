resource "aws_subnet" "subnet-a" {
  vpc_id            = var.vpc_id
  cidr_block        = var.cidr_block_a
  availability_zone = "eu-central-1a"
}

resource "aws_subnet" "subnet-b" {
  vpc_id            = var.vpc_id
  cidr_block        = var.cidr_block_b
  availability_zone = "eu-central-1b"
}

resource "aws_db_subnet_group" "_" {
  subnet_ids = [aws_subnet.subnet-a.id, aws_subnet.subnet-b.id]
}
