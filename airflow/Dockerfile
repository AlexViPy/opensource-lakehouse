FROM apache/airflow:2.9.3

# Become root to install requirements
USER root
RUN apt-get update \
    && apt-get install -y libpq-dev python-dev-is-python3 git procps default-jre curl wget \
    && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ADD --chown=airflow:airflow requirements.txt requirements.txt

USER airflow
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir && \
    pip install --force-reinstall pyspark==3.3.2 