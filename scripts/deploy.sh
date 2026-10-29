#!/bin/sh
# Deploys one commit on the server. GitHub Actions runs it over SSH as the deploy
# user: its key in ~/.ssh/authorized_keys is restricted to this script, and the
# "command" it sends (the commit SHA) arrives in SSH_ORIGINAL_COMMAND. It can also
# be run by hand: scripts/deploy.sh <commit-sha>
#
# The image for that commit was already built and pushed to ghcr.io by CI; this
# checks out the same commit, pulls the image and restarts the stack.

# Everything is inside main() so the shell has read the whole file before
# `git reset` below replaces it with the new version.
main() {
  set -eu
  sha="${SSH_ORIGINAL_COMMAND:-${1:-}}"
  case "$sha" in
    "" | *[!0-9a-f]*) echo "usage: deploy.sh <40-character commit sha>" >&2; exit 2 ;;
  esac
  if [ "${#sha}" -ne 40 ]; then
    echo "usage: deploy.sh <40-character commit sha>" >&2
    exit 2
  fi

  cd "$HOME/geomario_personal"
  compose="docker compose -f docker-compose.deploy.yml"

  echo "Checking out $sha"
  git fetch --quiet origin main
  git reset --quiet --hard "$sha"

  # Record the tag in .env, so manual compose commands use the same image.
  if grep -q '^APP_TAG=' .env; then
    sed -i "s|^APP_TAG=.*|APP_TAG=$sha|" .env
  else
    printf '\n# Image deployed by scripts/deploy.sh\nAPP_TAG=%s\n' "$sha" >> .env
  fi

  echo "Pulling the app image"
  $compose pull --quiet app
  # proxy and certbot are small and rarely change; build them here (cached).
  $compose build --quiet proxy certbot
  $compose up -d --no-build --remove-orphans
  docker image prune -f > /dev/null

  # The app runs migrations before gunicorn starts, so give it a moment.
  domain="$(grep '^DOMAIN=' .env | cut -d= -f2)"
  echo "Checking https://$domain/"
  curl -fsS -o /dev/null --retry 12 --retry-delay 5 --retry-all-errors \
    --resolve "$domain:443:127.0.0.1" "https://$domain/"
  echo "Deployed $sha"
}

main "$@"
exit
