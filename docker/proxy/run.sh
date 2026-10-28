#!/bin/sh

set -e

echo "Checking for dhparams.pem"
if [ ! -f "/vol/proxy/ssl-dhparams.pem" ]; then
  echo "dhparams.pem does not exist - creating it"
  openssl dhparam -out /vol/proxy/ssl-dhparams.pem 2048
fi

# Only substitute our own variables, so nginx's ($host, $remote_addr...) survive.
VARS='${DOMAIN} ${APP_HOST} ${APP_PORT}'

echo "Checking for fullchain.pem"
if [ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
  echo "No SSL cert, enabling HTTP only..."
  envsubst "$VARS" < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
else
  echo "SSL cert exists, enabling HTTPS..."
  envsubst "$VARS" < /etc/nginx/default-ssl.conf.tpl > /etc/nginx/conf.d/default.conf
fi

nginx -g 'daemon off;'
