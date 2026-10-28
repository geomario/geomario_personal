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

server {
    listen      443 ssl;
    http2       on;
    server_name ${DOMAIN};

    ssl_certificate     /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

    include     /etc/nginx/options-ssl-nginx.conf;

    ssl_dhparam /vol/proxy/ssl-dhparams.pem;

    # Not includeSubDomains: other subdomains of the domain may not serve HTTPS.
    add_header Strict-Transport-Security "max-age=31536000" always;

    client_max_body_size 10M;

    # Static files are served by whitenoise inside the app.
    location / {
        proxy_pass         http://${APP_HOST}:${APP_PORT};
        proxy_set_header   Host $host;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        # Always overwritten here, so clients can't spoof it; Django trusts it
        # because DJANGO_BEHIND_HTTPS_PROXY=1.
        proxy_set_header   X-Forwarded-Proto https;
    }
}
