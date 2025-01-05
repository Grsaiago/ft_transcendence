FROM debian:latest

RUN apt-get update && apt-get install -y curl

COPY ./docker/elastic_initializer/elastic_initializer.sh /usr/bin/

RUN chmod +x /usr/bin/elastic_initializer.sh

ENTRYPOINT [ "/usr/bin/elastic_initializer.sh" ]
