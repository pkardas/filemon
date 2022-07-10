module "vpc" {
  source   = "./modules/vpc"
  vpc_cidr = "10.0.0.0/16"
  subnet_id = aws_subnet.subnet-ec2.id

  route = [
    {
      cidr_block     = "0.0.0.0/0"
      gateway_id     = module.vpc.gateway_id
      nat_gateway_id = null
    }
  ]
}

resource "aws_security_group" "ec2" {
  name = "ec2-sg"

  description = "EC2 security group (terraform-managed)"
  vpc_id      = module.vpc.id

  ingress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds" {
  name = "rds-sg"

  description = "RDS (terraform-managed)"
  vpc_id      = module.vpc.id

  # Only PostgreSQL in
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2.id]
  }

  # Allow all outbound traffic.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_subnet" "subnet-ec2" {
  vpc_id            = module.vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-central-1a"
}

module "ec2" {
  source = "./modules/ec2"

  ami           = "ami-06cac34c3836ff90b"
  key_name      = "ec2-key"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet-ec2.id

  vpc_security_group_ids = [aws_security_group.ec2.id]
}

module "subnet_rds" {
  source = "./modules/subnet"

  cidr_block_a = "10.0.2.0/24"
  cidr_block_b = "10.0.3.0/24"
  vpc_id       = module.vpc.id
}

module "rds" {
  source = "./modules/rds"

  engine         = "postgres"
  engine_version = "14.2"

  instance_class = "db.t3.micro"

  allocated_storage = 10

  username = "filemon"
  password = var.db_password

  subnet_ids             = module.subnet_rds.ids
  vpc_security_group_ids = [aws_security_group.rds.id]

  multi_az          = false
  availability_zone = "eu-central-1a"
}
