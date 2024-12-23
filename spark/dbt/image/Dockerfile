ARG build_for=linux/amd64
FROM --platform=$build_for python:3.10.3-slim-bullseye as base

RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install -y --no-install-recommends \
    git \
    ssh-client \
    software-properties-common \
    make \
    build-essential \
    ca-certificates \
    libpq-dev \
  && apt-get clean \
  && rm -rf \
    /var/lib/apt/lists/* \
    /tmp/* \
    /var/tmp/*

ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

RUN python -m pip install --upgrade pip setuptools wheel poetry --no-cache-dir
COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry lock
RUN poetry install 

# Set docker basics
WORKDIR /usr/app/dbt/
COPY ["profiles.yml", "dbt_project.yml", "packages.yml", "./"]

FROM base as dbt-spark
RUN dbt debug --config-dir && dbt deps
CMD ["poetry", "run"]