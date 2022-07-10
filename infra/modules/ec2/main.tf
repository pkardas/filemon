resource "aws_instance" "_" {
  ami                         = var.ami
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  key_name                    = aws_key_pair._.key_name
  vpc_security_group_ids      = var.vpc_security_group_ids
}

resource "aws_eip" "_" {
  vpc      = true
  instance = aws_instance._.id
}

resource "tls_private_key" "_" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "_" {
  key_name   = var.key_name
  public_key = tls_private_key._.public_key_openssh
}
