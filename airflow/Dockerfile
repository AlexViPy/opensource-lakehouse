FROM apache/airflow:2.9.3

# Become root to install requirements
USER root
RUN apt-get update && apt-get install -y libpq-dev python-dev-is-python3 curl wget 
# vault settings
# RUN wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
# RUN echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
# RUN apt-get update && apt-get install vault
ADD --chown=airflow:airflow requirements.txt requirements.txt

USER airflow
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir