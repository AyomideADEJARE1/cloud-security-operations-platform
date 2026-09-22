resource "aws_db_subnet_group" "database" {
  name = "cloud-security-database-subnet-group"

  subnet_ids = [
    aws_subnet.private.id
  ]

  tags = {
    Name        = "cloud-security-database-subnet-group"
    Environment = "lab"
    Project     = "cloud-security-operations-platform"
  }
}


resource "aws_db_instance" "database" {
  identifier = "cloud-security-database"

  engine         = "mysql"
  engine_version = "8.0"

  instance_class = "db.t3.micro"

  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = "cloudsecurity"
  username = "admin"
  password = "CloudSecurityLab123!"

  db_subnet_group_name   = aws_db_subnet_group.database.name
  vpc_security_group_ids = [aws_security_group.database.id]

  publicly_accessible = false

  skip_final_snapshot = true

  tags = {
    Name        = "cloud-security-database"
    Environment = "lab"
    Project     = "cloud-security-operations-platform"
    Tier        = "database"
  }
}
