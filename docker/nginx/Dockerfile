FROM nginx:latest

# Install dependencies and setup env
RUN apt-get update && apt install -y openssl

COPY ./docker/nginx/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
