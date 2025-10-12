terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.47"
    }
  }
}

provider "hcloud" {
  token = var.hetzner_token
}

variable "hetzner_token" { type = string }
variable "pg_name"       { type = string  default = "heartlink-prod" }
variable "pg_version"    { type = string  default = "16" }
variable "pg_tier"       { type = string  default = "basic" } # basic/standard/high-memory
variable "pg_location"   { type = string  default = "nbg1" }   # EU datacenter

# NOTE: Managed DB resources would be defined here when using Hetzner's provider for databases.

output "notes" {
  value = "Add hcloud_database resources here when enabling Managed Postgres."
}
