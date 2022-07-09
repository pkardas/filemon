resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "private-subnet" {
  vpc_id            = aws_vpc.vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = var.availability-zone
}

resource "aws_db_subnet_group" "db-subnet" {
  subnet_ids = [aws_subnet.private-subnet.id]
}

resource "aws_db_instance" "database-instance" {
  instance_class       = "db.t2.micro"
  engine               = "postgres"
  engine_version       = "14.3"
  availability_zone    = var.availability-zone
  db_subnet_group_name = aws_db_subnet_group.db-subnet.name
  multi_az             = false
  username             = "filemon"
  password             = var.db_password
}
