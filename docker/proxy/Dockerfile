FROM nginx:1.30-alpine

COPY ./nginx/* /etc/nginx/
COPY ./run.sh /run.sh

ENV APP_HOST=app
ENV APP_PORT=8000

RUN apk add --no-cache openssl && \
    chmod +x /run.sh

VOLUME /vol/www

CMD ["/run.sh"]
