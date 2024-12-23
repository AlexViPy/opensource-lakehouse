ARG OPENJDK_VERSION=8
FROM eclipse-temurin:${OPENJDK_VERSION}-jre

ARG BUILD_DATE
ARG SPARK_VERSION=3.4.2
ARG HADOOP_VERSION=3

LABEL org.label-schema.name="Apache Spark ${SPARK_VERSION}" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.version=$SPARK_VERSION

ENV SPARK_HOME /usr/spark
ENV PATH="/usr/spark/bin:/usr/spark/sbin:${PATH}"

RUN apt-get update && \
    apt-get install -y wget netcat procps libpostgresql-jdbc-java && \
    wget -q "http://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    tar xzf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    mv "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" /usr/spark && \
    ln -s /usr/share/java/postgresql-jdbc4.jar /usr/spark/jars/postgresql-jdbc4.jar

# Download delta jar
RUN wget -q "https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar" && \
    wget -q "https://repo1.maven.org/maven2/io/delta/delta-storage/2.4.0/delta-storage-2.4.0.jar" && \
    wget -q "https://repo1.maven.org/maven2/io/delta/delta-hive_2.12/0.6.0/delta-hive_2.12-0.6.0.jar" && \
    mv delta-core_2.12-2.4.0.jar /usr/spark/jars/ && \
    mv delta-storage-2.4.0.jar /usr/spark/jars/ && \
    mkdir -p /usr/hive/jars && mv delta-hive_2.12-0.6.0.jar /usr/hive/jars/

# Install Iceberg
# RUN wget -q "https://search.maven.org/remotecontent?filepath=org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.5.0/iceberg-spark-runtime-3.5_2.12-1.5.0.jar" && \
#     mv remotecontent?filepath=org%2Fapache%2Ficeberg%2Ficeberg-spark-runtime-3.5_2.12%2F1.5.0%2Ficeberg-spark-runtime-3.5_2.12-1.5.0.jar /usr/spark/jars/

# Install s3 libs
# RUN wget -q "https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar" && \
#     wget -q "https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.681/aws-java-sdk-bundle-1.12.681.jar" && \
#     mv hadoop-aws-3.3.6.jar /usr/spark/jars/ && \
#     mv aws-java-sdk-bundle-1.12.681.jar /usr/spark/jars/

# Clean up
RUN apt-get remove -y wget && \
    apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /scripts/
RUN chmod +x /scripts/entrypoint.sh

ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["--help"]