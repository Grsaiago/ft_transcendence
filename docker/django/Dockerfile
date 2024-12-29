# Multistage with final build not including poetry
FROM python:3.12.1-bullseye AS build

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

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

WORKDIR /app

COPY --from=build /build/requirements.txt /build/constraints.txt ./

RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt

WORKDIR /app/ft_transcendence

COPY ./ft_transcendence/ .

COPY ./docker/django/entrypoint.sh ./

RUN chmod +x ./entrypoint.sh

# TODO: Make entrypoint into a script for initialization, the script will run migrations, collect static, apply translations etc etc
# AND THEN RUN THE BELOW ENTRYPOINT USING EXEC IN THE SHELLSCRIPT
ENTRYPOINT ["./entrypoint.sh"]

# # Single stage with final build including poetry
# FROM python:3.12.1-bullseye
#
# RUN apt-get update && apt-get install -y \
# 	curl \
# 	build-essential \
# 	libpq-dev
#
# RUN curl -sSL https://install.python-poetry.org | python3 -
#
# ENV PATH="/root/.local/bin:$PATH"
#
# WORKDIR /app
#
# # Those first copy and run directives are set up separatelly from the other
# # two so we can get the most out of Docker's cache system for builds.
# COPY pyproject.toml poetry.lock /app/
#
# # package mode is already set as false in our pyproject.toml
# # (https://python-poetry.org/docs/basic-usage/#operating-modes)
# RUN poetry install 
#
# WORKDIR /app/ft_transcendence
#
# COPY ./ft_transcendence/ .
#
# ENTRYPOINT [ "poetry", "run", "/app/ft_trascendence/manage.py", "runserver"]


