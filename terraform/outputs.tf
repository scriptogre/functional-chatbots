output "ec2_instance_id" {
  description = "The ID of the EC2 instance running the application"
  value       = aws_instance.web.id
}

output "load_balancer_dns_name" {
  description = "The DNS name of the load balancer."
  value       = aws_lb.this.dns_name
}

output "acm_certificate_arn" {
  description = "The ARN of the ACM certificate used for HTTPS."
  value       = aws_acm_certificate.this.arn
}

output "security_group_id" {
  description = "The ID of the security group attached to the EC2 instance."
  value       = aws_security_group.web.id
}

output "ec2_instance_public_ip" {
  description = "The public IP address of the EC2 instance."
  value       = aws_instance.web.public_ip
}

output "ec2_instance_public_dns" {
  description = "The public DNS name of the EC2 instance."
  value       = aws_instance.web.public_dns
}
