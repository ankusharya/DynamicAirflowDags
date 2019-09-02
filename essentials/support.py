from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator


class Support():
    def __init__(self):
        pass

    def supported_operators(self):
        operators = {
            "ssh": SSHOperator,
            "bash": BashOperator,
            "python": PythonOperator,
            "postgres": PostgresOperator,
            "branch_python": BranchPythonOperator
        }
        return operators

    def supported_groups(self):
        return ["pre_validation", "ingestion", "post_validation"]
