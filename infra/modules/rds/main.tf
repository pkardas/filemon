resource "aws_db_subnet_group" "_" {
  name       = "subnet-group"
  subnet_ids = var.subnet_ids
}

resource "aws_db_instance" "_" {
  engine         = var.engine
  engine_version = var.engine_version

  instance_class = var.instance_class

  allocated_storage   = var.allocated_storage

  username = var.username
  password = var.password

  db_subnet_group_name   = aws_db_subnet_group._.name
  vpc_security_group_ids = var.vpc_security_group_ids

  multi_az          = var.multi_az
  availability_zone = var.availability_zone
}
