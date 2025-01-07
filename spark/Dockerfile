FROM bitnami/spark:3.3.2

USER root
ENV HIVE_HOME=/opt/bitnami/spark
RUN apt-get update && apt-get install -y curl

COPY ./jars/* $HIVE_HOME/jars