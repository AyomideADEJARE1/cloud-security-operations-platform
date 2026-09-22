resource "aws_instance" "app" {
  ami           = "ami-ubuntu2404-amd64"
  instance_type = "t3.micro"

  subnet_id = aws_subnet.public.id

  vpc_security_group_ids = [
    aws_security_group.app.id
  ]

  lifecycle {
    ignore_changes = [
      vpc_security_group_ids
    ]
  }

  tags = {
    Name        = "cloud-security-app-server"
    Environment = "lab"
    Project     = "cloud-security-operations-platform"
    Role        = "application"
  }
}
