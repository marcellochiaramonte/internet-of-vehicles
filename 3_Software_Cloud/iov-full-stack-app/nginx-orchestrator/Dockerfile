FROM nginx:1.19.3-alpine

COPY nginx.conf /etc/nginx/nginx.conf

COPY ./certs /etc/nginx/certs

COPY ./site/index.html /usr/share/nginx/site/html/index.html