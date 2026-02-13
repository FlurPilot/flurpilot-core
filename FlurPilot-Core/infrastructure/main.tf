# Terraform configuration for FlurPilot (Hetzner Cloud)
terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.45"
    }
  }
}

provider "hcloud" {
  # Token sourced from HCLOUD_TOKEN environment variable
}

# 1. Firewall (Security First)
resource "hcloud_firewall" "flurpilot_fw" {
  name = "flurpilot-fw"

  # SSH (DISABLED: Use VPN or Hetzner Console)
  # rule {
  #   direction = "in"
  #   protocol  = "tcp"
  #   port      = "22"
  #   source_ips = [
  #     "0.0.0.0/0",
  #     "::/0"
  #   ]
  # }

  # HTTP
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "80"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
  }

  # HTTPS
  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "443"
    source_ips = [
      "0.0.0.0/0",
      "::/0"
    ]
  }
}

# 2. Volume (Persistent Data for PostGIS)
resource "hcloud_volume" "flurpilot_data" {
  name      = "flurpilot-data"
  size      = 10 # GB
  location  = "fsn1"
  format    = "ext4"
  automount = true
}

# 3. Server (The Worker)
resource "hcloud_server" "web_01" {
  name        = "flurpilot-core-v1"
  image       = "ubuntu-24.04"
  server_type = "cx22" # 2 vCPU, 4GB RAM
  location    = "fsn1"

  firewall_ids = [hcloud_firewall.flurpilot_fw.id]
  backups      = true

  # Bootstrapping (Docker, Users)
  user_data = file("${path.module}/cloud-init.yml")

  public_net {
    ipv4_enabled = true
    ipv6_enabled = true
  }
}

# 4. Attachment
resource "hcloud_volume_attachment" "main" {
  volume_id = hcloud_volume.flurpilot_data.id
  server_id = hcloud_server.web_01.id
  automount = true
}

output "ipv4_address" {
  value = hcloud_server.web_01.ipv4_address
}
