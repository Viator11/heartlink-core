terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

variable "cloudflare_api_token" { type = string }
variable "cloudflare_account_id" { type = string }
variable "zone" { type = string  default = "heartlink.love" }

# Zone data
data "cloudflare_zone" "this" {
  name = var.zone
}

# Subdomains
locals {
  records = [
    { name = "app",   type = "CNAME", value = "your.app.host"  },
    { name = "api",   type = "CNAME", value = "your.api.host"  },
    { name = "stage", type = "CNAME", value = "your.stage.host"},
    { name = "cdn",   type = "CNAME", value = "your.cdn.host"  },
    { name = "mail",  type = "CNAME", value = "your.mail.host" },
  ]
}

resource "cloudflare_record" "records" {
  for_each = { for r in local.records : r.name => r }
  zone_id  = data.cloudflare_zone.this.id
  name     = each.value.name
  type     = each.value.type
  value    = each.value.value
  proxied  = true
}

# R2 bucket (skeleton via API)
# Note: R2 buckets are managed at the account level; Terraform support is limited.
# We'll declare bucket name via variables and bind via Workers/Routes later.
variable "r2_bucket_name" { type = string  default = "heartlink-media" }
output "zone_id" { value = data.cloudflare_zone.this.id }
