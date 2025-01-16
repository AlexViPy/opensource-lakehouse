ARG BUILD_FOR=linux/amd64
FROM --platform=$BUILD_FOR python:3.10.7-slim-bullseye as base

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

ENV DBT_CONNECTOR=dbt-spark
ENV DBT_PKG=1.9.0

RUN python -m pip install --upgrade pip setuptools wheel --no-cache-dir

# Set docker basics
WORKDIR /usr/app/dbt/
COPY ["profiles.yml", "dbt_project.yml", "packages.yml", "./"]
RUN pip install $DBT_CONNECTOR==$DBT_PKG \
                $DBT_CONNECTOR[PyHive] --no-cache-dir

FROM base as dbt-spark
RUN dbt debug --config-dir && dbt deps
CMD ["sleep", "infinity"]