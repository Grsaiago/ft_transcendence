FROM python:3.12.1-bullseye AS build

# Install dependencies and setup env
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /build

COPY ./pyproject.toml ./poetry.lock /build/

# add poetry's export plugin and export files used by pip
RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --without-hashes -o ./requirements.txt
RUN poetry export -f constraints.txt --without-hashes -o ./constraints.txt

FROM python:3.12.1 AS image

RUN apt-get update && apt-get install -y curl

COPY --from=build /build/requirements.txt /build/constraints.txt ./
RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt

COPY ./docker/initializer/entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh

WORKDIR /app/ft_transcendence

COPY ./ft_transcendence/ .

ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]
