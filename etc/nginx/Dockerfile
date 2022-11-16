FROM nginx:1.21-alpine
WORKDIR /etc/nginx/templates

ARG BACKEND_URL
ENV BACKEND_URL=$BACKEND_URL

COPY templates/backend.conf.template ./backend.conf.template
CMD ["nginx","-g","daemon off;"]
