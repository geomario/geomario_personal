server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }

    location / {
        return 301 https://${DOMAIN}$request_uri;
    }
}

# First HTTPS server, so it is also the default for unknown host names
# (Django then rejects them with 400).
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

# www.<domain> uses the same certificate and redirects to the bare domain.
server {
    listen      443 ssl;
    http2       on;
    server_name www.${DOMAIN};

    ssl_certificate     /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

    include     /etc/nginx/options-ssl-nginx.conf;

    ssl_dhparam /vol/proxy/ssl-dhparams.pem;

    add_header Strict-Transport-Security "max-age=31536000" always;

    return 301 https://${DOMAIN}$request_uri;
}
