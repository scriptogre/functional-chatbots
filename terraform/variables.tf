variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro" # Choose an appropriate instance type
}

variable "ami" {
  description = "The AMI to use for the instance"
  default     = "ami-064573ac645743ea8"
}

variable "dockerhub_username" {
  description = "DockerHub username for pulling images"
  type        = string
  sensitive   = true
}

variable "dockerhub_password" {
  description = "DockerHub password for pulling images"
  type        = string
  sensitive   = true
}

variable "groq_api_key" {
  description = "GroqCloud API"
  type        = string
  sensitive   = true
}

variable "namecheap_user_name" {
  description = "Namecheap username for updating DNS records"
  type        = string
}

variable "namecheap_api_user" {
  description = "Namecheap API user for updating DNS records"
  type        = string
  sensitive   = true
}

variable "namecheap_api_key" {
  description = "Namecheap API key for updating DNS records"
  type        = string
  sensitive   = true
}
