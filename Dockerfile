FROM puckel/docker-airflow:1.10.2
ARG AIRFLOW_HOME=/usr/local/airflow

USER root

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && pip install psycopg2-binary

COPY dags/ ${AIRFLOW_HOME}/dags/
COPY essentials/ ${AIRFLOW_HOME}/essentials/

USER airflow
WORKDIR ${AIRFLOW_HOME}