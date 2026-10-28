terraform {
  required_version = "~> 1.15"

  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.70"
    }
  }

  # State is a local file (infra/terraform.tfstate, git-ignored): one person, one
  # server. If it's lost, re-import the three resources with `terraform import`.
}
