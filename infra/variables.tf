variable "name" {
  description = "Name of the server and prefix for the other resources."
  type        = string
  default     = "geomario"
}

variable "server_type" {
  description = "Hetzner Cloud server type."
  type        = string
  default     = "cpx02"
}

variable "location" {
  description = "Hetzner location: nbg1 (Nuremberg), fsn1 (Falkenstein) or hel1 (Helsinki)."
  type        = string
  default     = "nbg1"
}

variable "image" {
  description = "Operating system image."
  type        = string
  default     = "ubuntu-24.04"
}

variable "ssh_public_key_path" {
  description = "Public SSH key allowed to log in (mounted read-only by docker-compose.yml)."
  type        = string
  default     = "/ssh/id.pub"
}

variable "ssh_source_ips" {
  description = "Addresses allowed to reach SSH. Open by default because GitHub Actions deploys over SSH; login is key-only."
  type        = list(string)
  default     = ["0.0.0.0/0", "::/0"]
}
