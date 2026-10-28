output "ipv4_address" {
  description = "Use this for the A record of the domain at GoDaddy."
  value       = hcloud_server.web.ipv4_address
}

output "ssh" {
  description = "Log in as root (the deploy user exists too, for CI)."
  value       = "ssh root@${hcloud_server.web.ipv4_address}"
}
