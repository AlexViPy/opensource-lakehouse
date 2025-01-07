FROM openjdk:8u342-jre

# Lifted from: https://github.com/joshuarobinson/presto-on-k8s/blob/1c91f0b97c3b7b58bdcdec5ad6697b42e50d74c7/hive_metastore/Dockerfile

# see https://hadoop.apache.org/releases.html
ARG HADOOP_VERSION=3.2.0
# see https://downloads.apache.org/hive/
ARG HIVE_METASTORE_VERSION=3.0.0
# see https://jdbc.postgresql.org/download.html#current
ARG POSTGRES_CONNECTOR_VERSION=42.2.18

# Set necessary environment variables.
ENV HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
ENV HIVE_HOME=/opt/apache-hive-metastore-${HIVE_METASTORE_VERSION}-bin
ENV PATH=/opt/spark/bin:/opt/hadoop/bin:${PATH}
RUN apt-get update && \
    apt-get install -y net-tools telnet curl

WORKDIR /opt

# hadolint ignore=DL3008
RUN curl -L https://apache.org/dist/hive/hive-standalone-metastore-${HIVE_METASTORE_VERSION}/hive-standalone-metastore-${HIVE_METASTORE_VERSION}-bin.tar.gz | tar zxf - && \
    curl -L https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | tar zxf - && \
    curl -L https://jdbc.postgresql.org/download/postgresql-$POSTGRES_CONNECTOR_VERSION.jar --output /opt/postgresql-$POSTGRES_CONNECTOR_VERSION.jar && \
    cp /opt/postgresql-$POSTGRES_CONNECTOR_VERSION.jar ${HIVE_HOME}/lib/

COPY ./metastore-site.xml ${HIVE_HOME}/conf
COPY ./entrypoint.sh /entrypoint.sh

RUN groupadd -r hive --gid=1000 && \
    useradd -r -g hive --uid=1000 -d ${HIVE_HOME} hive && \
    chown hive:hive -R ${HIVE_HOME} && \
    chown hive:hive /entrypoint.sh && chmod +x /entrypoint.sh

RUN echo "Purge build artifacts" && \
    apt-get purge -y --auto-remove curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER hive
EXPOSE 9083

ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]