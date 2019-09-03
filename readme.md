### DynamicAirflowDags
This repository generates dynamic dags based on given json file.

## Prerequisites
Apache Airflow
### Supported Operators
1. Bash Operator
2. Python Operator
3. Branch Python Operator
4. Postgres Operator
5. SSH Operator

### Setup
1. AIRFLOW_HOME should be in your PYTHONPATH/ sys.path
2. Copy and paste *dynamic_dag.py* in DAG folder
3. Copy and paste *essentials* package directly under AIRFLOW_HOME

### Docker setup
1. Install Docker and Docker Compose
2. Clone this repository
3. Run command
```bash
docker-compose -f dynamic-dag-airflow.yaml up
```
Note: Docker compose file is based on [puckel/docker-airflow](https://github.com/puckel/docker-airflow)

