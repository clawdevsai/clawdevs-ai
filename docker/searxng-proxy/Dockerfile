FROM nginx:1.27-alpine

RUN apk upgrade --no-cache \
    && apk del --no-cache \
        curl \
        libcurl \
        c-ares \
        nghttp2-libs \
        nginx-module-geoip \
        nginx-module-image-filter \
        nginx-module-njs \
        nginx-module-xslt

COPY docker/searxng-proxy/default.conf /etc/nginx/conf.d/default.conf
