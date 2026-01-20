FROM nginx:alpine
RUN rm -rf /usr/share/nginx/html/*
COPY ./src /usr/share/nginx/html
RUN chmod -R 755 /usr/share/nginx/html
EXPOSE 80