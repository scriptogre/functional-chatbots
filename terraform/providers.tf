terraform {
  required_providers {
    namecheap = {
      source = "namecheap/namecheap"
      version = "2.1.2"
    }
    aws = {
      source = "hashicorp/aws"
      version = "5.40.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

provider "namecheap" {
  user_name = var.namecheap_user_name
  api_user  = var.namecheap_api_user
  api_key  = var.namecheap_api_key
  client_ip = "86.124.116.177"
}