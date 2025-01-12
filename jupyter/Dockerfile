FROM jupyter/pyspark-notebook:spark-3.3.2
USER root

# add needed packages
RUN apt-get update && apt-get install python3-boto3 -y

# Install Python requirements
COPY ./requirements.txt /home/jovyan/
RUN pip install -r /home/jovyan/requirements.txt --no-cache-dir

COPY jupyter_lab_config.json /home/jovyan/