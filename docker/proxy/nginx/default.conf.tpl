# Used until a certificate exists: answers Let's Encrypt's challenge and
# sends everything else to HTTPS.
server {
    listen 80;
    server_name ${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
