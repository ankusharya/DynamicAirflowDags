import sys
sys.path.insert(0, '/usr/local/airflow')

from airflow.models import DAG
from essentials.load_dag import LoadDags
from essentials.load_json import LoadJSON

input_dag = LoadJSON().load_json_dict()
for single_dag in input_dag:
    dag_id, dag = LoadDags(single_dag).construct_dag()
    globals()[dag_id] = dag
