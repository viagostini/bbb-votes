FROM python:3.9.12-slim

WORKDIR /usr/src

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.1.13 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/usr/src/poetry_cache/ 

RUN groupadd -r bbb-votes && useradd --no-log-init -u 1000 -r -g bbb-votes bbb-votes

RUN mkdir /var/log/bbb-votes && chown bbb-votes:bbb-votes /var/log/bbb-votes

RUN apt-get update -qq && apt-get --no-install-recommends -y -qq install python-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN poetry install

USER bbb-votes
