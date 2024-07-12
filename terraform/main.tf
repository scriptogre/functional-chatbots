resource "namecheap_domain_records" "this" {
  domain = "tanulchristian.dev"

  record {
    hostname    = "functional-chatbots"
    type    = "ALIAS"
    address = aws_lb.this.dns_name
    ttl     = 60
  }

  dynamic "record" {
    for_each = { for dvo in aws_acm_certificate.this.domain_validation_options : dvo.domain_name => {
      name  = trimsuffix(dvo.resource_record_name, ".tanulchristian.dev.")
      type  = dvo.resource_record_type
      value = dvo.resource_record_value
    }}

    content {
      hostname = record.value.name
      type     = record.value.type
      address  = record.value.value
      ttl      = 60
    }
  }
}

# Create ACM certificate for the domain
resource "aws_acm_certificate" "this" {
  domain_name       = "functional-chatbots.tanulchristian.dev"
  validation_method = "DNS"
}


# Security group configuration to define ingress and egress rules for the EC2 instance.
resource "aws_security_group" "web" {
  vpc_id      = data.aws_vpc.this.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_lb" "this" {
  internal           = false
  load_balancer_type = "application"
  subnets            = [data.aws_subnet.public1.id, data.aws_subnet.public2.id]
  security_groups    = [aws_security_group.web.id]

  enable_deletion_protection = false

  tags = {
    Name = "Application Load Balancer"
  }
}


# Listener for HTTP traffic
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  # Default action is to redirect all HTTP traffic to HTTPS
  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}


resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.this.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate.this.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_tg.arn
  }
}


data "aws_vpc" "this" {
  default = true
}

data "aws_subnet" "public1" {
  vpc_id            = data.aws_vpc.this.id
  availability_zone = "eu-central-1a"
}

data "aws_subnet" "public2" {
  vpc_id            = data.aws_vpc.this.id
  availability_zone = "eu-central-1b"
}

resource "aws_lb_target_group" "app_tg" {
  name     = "functional-chatbots-target-group"
  port     = 80  # The port your application is listening on; adjust if necessary
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.this.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    path                = "/"  # Adjust if your application has a different health check endpoint
    protocol            = "HTTP"
    interval            = 30
    matcher             = "200"
  }
}

resource "aws_lb_target_group_attachment" "this" {
  target_group_arn = aws_lb_target_group.app_tg.arn
  target_id        = aws_instance.web.id
  port             = 80
}

# EC2 instance configuration including the setup for Docker and running a Docker container on instance start.
resource "aws_instance" "web" {
  ami                    = var.ami
  instance_type          = var.instance_type
  key_name               = "scriptogre"
  vpc_security_group_ids = [aws_security_group.web.id]

  user_data = <<-EOF
              #!/bin/bash
              echo "Updating and installing Docker..."
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -a -G docker ec2-user

              echo "Creating .env file..."
              cat <<EOT >> /home/ec2-user/.env
              GROQ_API_KEY=${var.groq_api_key}
              EOT

              # Login to DockerHub
              echo "Logging into DockerHub..."
              docker login -u "${var.dockerhub_username}" -p "${var.dockerhub_password}"

              # Define an alias for managing Docker containers
              echo "Creating Docker management alias..."
              echo "alias docker_refresh='docker stop \$(docker ps -aq) && docker rm \$(docker ps -aq) && docker pull ${var.dockerhub_username}/functional-chatbots:latest && docker run --platform linux/amd64 -d -p 80:8000 -p 443:8000 --env-file /home/ec2-user/.env ${var.dockerhub_username}/functional-chatbots:latest'" >> /home/ec2-user/.bashrc

              # Run the Docker container
              echo "Starting Docker container..."
              docker run --platform linux/amd64 -d -p 80:8000 -p 443:8000 \
                  --env-file /home/ec2-user/.env \
                  ${var.dockerhub_username}/functional-chatbots:latest > /var/log/app.log 2>&1
              EOF

  tags = {
    Name = "Web Instance for functional-chatbots.tanulchristian.dev"
  }

  # don't force-recreate instance if only user models changes
  lifecycle {
    ignore_changes = [user_data]
  }
}