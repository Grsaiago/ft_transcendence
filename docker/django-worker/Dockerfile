# Multistage with final build not including poetry
FROM python:3.12.1-bullseye AS build

# Install dependencies and setup env
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /build

COPY ./pyproject.toml ./poetry.lock /build/

# add poetry's export plugin
RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --without-hashes -o ./requirements.txt
RUN poetry export -f constraints.txt --without-hashes -o ./constraints.txt

# final stage
FROM python:3.12.1-bullseye AS image

RUN apt-get update && apt-get install -y \
	curl \
	build-essential \
	libpq-dev \
	gettext

WORKDIR /app

COPY --from=build /build/requirements.txt /build/constraints.txt ./

RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt
RUN pip install --no-cache-dir 'Twisted[tls,http2]'

WORKDIR /app/ft_transcendence

COPY ./ft_transcendence/ .

COPY ./docker/django-worker/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
