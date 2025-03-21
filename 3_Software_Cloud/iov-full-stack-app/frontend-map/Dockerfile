FROM node:15.7.0-alpine AS builder

WORKDIR /usr/src/app

COPY ./iov-frontend/package.json .
COPY ./iov-frontend/package-lock.json .

RUN npm install

COPY ./iov-frontend .

RUN npm run build


FROM nginx:1.19.6-alpine

# RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf

COPY --from=builder /usr/src/app/dist/iov-frontend /usr/share/nginx/html

