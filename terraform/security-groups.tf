resource "aws_security_group" "app" {
  name        = "cloud-security-app-sg"
  description = "Security group for the application server"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name        = "cloud-security-app-sg"
    Environment = "lab"
    Tier        = "application"
  }
}

resource "aws_security_group" "database" {
  name        = "cloud-security-database-sg"
  description = "Security group for the database"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name        = "cloud-security-database-sg"
    Environment = "lab"
    Tier        = "database"
  }
}

resource "aws_vpc_security_group_ingress_rule" "app_http" {
  security_group_id = aws_security_group.app.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 80
  ip_protocol = "tcp"
  to_port     = 80

  description = "Allow HTTP web traffic"
}

resource "aws_vpc_security_group_ingress_rule" "app_https" {
  security_group_id = aws_security_group.app.id

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  ip_protocol = "tcp"
  to_port     = 443

  description = "Allow HTTPS web traffic"
}

resource "aws_vpc_security_group_ingress_rule" "database_mysql" {
  security_group_id = aws_security_group.database.id

  referenced_security_group_id = aws_security_group.app.id

  from_port   = 3306
  ip_protocol = "tcp"
  to_port     = 3306

  description = "Allow MySQL traffic from application servers"

  lifecycle {
    ignore_changes = [
      referenced_security_group_id
    ]
  }
}
