# Multistage with final build not including poetry
FROM python:3.12.1-bullseye AS build

# create certificate directory
RUN mkdir /cert

# Install dependencies and setup env
RUN apt-get update && apt install -y openssl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# generate certificates
RUN openssl req -x509 -newkey rsa:2048 -keyout /cert/key.pem -out /cert/cert.pem -days 365 -nodes \
	-subj "/C=BR/ST=RioDeJaneiro/L=RioDeJaneiro/O=TrasncendenceDasMinasESaiago/OU=Unit/CN=localhost"

WORKDIR /build

COPY ./pyproject.toml ./poetry.lock /build/

RUN poetry export -f requirements.txt --without-hashes -o ./requirements.txt
RUN poetry export -f constraints.txt --without-hashes -o ./constraints.txt

# final stage
FROM python:3.12.1-bullseye AS image

RUN apt-get update && apt-get install -y \
	curl \
	build-essential \
	libpq-dev \
	gettext

# Copy certificates from build stage
COPY --from=build /cert/cert.pem /cert/key.pem /cert/

WORKDIR /app

COPY --from=build /build/requirements.txt /build/constraints.txt ./

RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt
RUN pip install --no-cache-dir 'Twisted[tls,http2]'

WORKDIR /app/ft_transcendence

COPY ./ft_transcendence/ .

COPY ./docker/django/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

# TODO: Make entrypoint into a script for initialization, the script will run migrations, collect static, apply translations etc etc
# AND THEN RUN THE BELOW ENTRYPOINT USING EXEC IN THE SHELLSCRIPT
ENTRYPOINT ["./entrypoint.sh"]
