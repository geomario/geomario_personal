#!/bin/sh
# Entry point for `docker compose run --rm terraform <command>`: initialises Terraform
# quietly and then runs the given command. Providers live in a Docker volume, so the
# container's Linux files never mix with the host's.
set -e
export TF_DATA_DIR=/terraform-data
terraform init -input=false > /dev/null
exec terraform "$@"
