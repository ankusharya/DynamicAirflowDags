from datetime import datetime
from airflow.models import DAG
from essentials.load_dag import LoadDags
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator


def test_construct_bash_task():
    input_task = {
        "operator": "bash",
        "task_id": "first_task",
        "command": "echo 'This is first task'",
        "dependency": "sequential",
        "load_from_app_config": "true"
    }

    default_args = {'owner': 'airflow',
                    'start_date': datetime(2018, 1, 1)
                    }
    dag = DAG("test_dag",
              schedule_interval=None,
              default_args=default_args)

    operator = LoadDags("").construct_task(input_task, "pre_validation", dag)

    assert operator.task_id == "pre_validation_first_task"
    assert isinstance(operator, BashOperator)
    assert operator.bash_command == "echo 'This is first task'"


def test_construct_ssh_task():
    input_task = {
        "operator": "ssh",
        "task_id": "ssh_task",
        "conn_id": "ssh_conn",
        "command": "echo 'This is ssh task'",
        "dependency": "sequential",
        "load_from_app_config": "true"
    }
    default_args = {'owner': 'airflow',
                    'start_date': datetime(2018, 1, 1)
                    }
    dag = DAG("test_dag",
              schedule_interval=None,
              default_args=default_args)

    operator = LoadDags("").construct_task(input_task, "pre_validation", dag)

    assert operator.task_id == "pre_validation_ssh_task"
    assert isinstance(operator, SSHOperator)
    assert operator.ssh_conn_id == "ssh_conn"
    assert operator.command == "echo 'This is ssh task'"


def test_construct_python_task():
    import types
    input_task = {
        "operator": "python",
        "task_id": "python_task",
        "function_name": "pow",
        "function_kwargs": {"a": 1, "b": 2},
        "dependency": "sequential",
        "load_from_app_config": "true"
    }
    default_args = {'owner': 'airflow',
                    'start_date': datetime(2018, 1, 1)
                    }
    dag = DAG("test_dag",
              schedule_interval=None,
              default_args=default_args)
    operator = LoadDags("").construct_task(input_task, "pre_validation", dag)

    assert isinstance(operator, PythonOperator)
    assert operator.task_id == "pre_validation_python_task"
    assert isinstance(operator.python_callable, types.BuiltinFunctionType)


def test_construct_postgres_task():
    input_task = {
        "operator": "postgres",
        "task_id": "postgres_task",
        "conn_id": "postgres_conn_id",
        "sql": "select * from table limit 10",
        "dependency": "sequential",
        "load_from_app_config": "true"
    }
    default_args = {'owner': 'airflow',
                    'start_date': datetime(2018, 1, 1)
                    }
    dag = DAG("test_dag",
              schedule_interval=None,
              default_args=default_args)
    operator = LoadDags("").construct_task(input_task, "pre_validation", dag)

    assert operator.task_id == "pre_validation_postgres_task"
    assert isinstance(operator, PostgresOperator)
    assert operator.postgres_conn_id == "postgres_conn_id"
    assert operator.sql == "select * from table limit 10"


def test_construct_branch_python_task():
    import types
    input_task = {
        "operator": "branch_python",
        "task_id": "python_branch_task",
        "function_name": "pow",
        "function_kwargs": {"a": 1, "b": 2},
        "dependency": "sequential",
        "load_from_app_config": "true"
    }
    default_args = {'owner': 'airflow',
                    'start_date': datetime(2018, 1, 1)
                    }
    dag = DAG("test_dag",
              schedule_interval=None,
              default_args=default_args)
    operator = LoadDags("").construct_task(input_task, "pre_validation", dag)

    assert operator.task_id == "pre_validation_python_branch_task"
    assert isinstance(operator, BranchPythonOperator)
    assert isinstance(operator.python_callable, types.BuiltinFunctionType)


def test_construct_group_task():
    input_group = [
        {
            "operator": "bash",
            "task_id": "first_task",
            "command": "echo 'This is first task'",
            "dependency": "sequential",
            "load_from_app_config": "true"
        },
        {
            "operator": "bash",
            "task_id": "second_task",
            "command": "echo 'This is second task'",
            "dependency": "sequential",
            "load_from_app_config": "true"
        }
    ]
    default_args = {'owner': 'airflow',
                    'start_date': datetime(2018, 1, 1)
                    }
    dag = DAG("test_dag",
              schedule_interval=None,
              default_args=default_args)

    one_group = LoadDags("").construct_one_group(input_group, "pre_validation", dag)
    second_group = LoadDags("").construct_one_group(input_group, "ingestion", dag)
    assert one_group[0].task_id == "pre_validation_first_task"
    assert one_group[1].task_id == "pre_validation_second_task"
    assert second_group[0].task_id == "ingestion_first_task"
    assert second_group[1].task_id == "ingestion_second_task"


def test_task_dependencies():
    input_group = [
        {
            "operator": "bash",
            "task_id": "first_task",
            "command": "echo 'This is first task'",
            "dependency": "sequential",
            "load_from_app_config": "true"
        },
        {
            "operator": "bash",
            "task_id": "second_task",
            "command": "echo 'This is second task'",
            "dependency": "sequential",
            "load_from_app_config": "true"
        }
    ]
    default_args = {'owner': 'airflow',
                    'start_date': datetime(2018, 1, 1)
                    }
    dag = DAG("test_dag",
              schedule_interval=None,
              default_args=default_args)

    one_group = LoadDags("").construct_one_group(input_group, "pre_validation", dag)
    second_group = LoadDags("").construct_one_group(input_group, "ingestion", dag)


def test_construct_dag():
    input_dag = {
        "dag_id": "dynamic_trigger_test",
        "pre_validation": [
            {
                "operator": "bash",
                "task_id": "first_task",
                "command": "echo 'This is first task'",
                "dependency": "sequential",
                "load_from_app_config": "true"
            },
            {
                "operator": "bash",
                "task_id": "second_task",
                "command": "echo 'This is second task'",
                "dependency": "sequential",
                "load_from_app_config": "true"
            }
        ],
        "post_validation": [
            {
                "operator": "bash",
                "task_id": "first_task",
                "command": "echo 'This is first task'",
                "dependency": "sequential",
                "load_from_app_config": "true"
            },
            {
                "operator": "bash",
                "task_id": "second_task",
                "command": "echo 'This is second task'",
                "dependency": "sequential",
                "load_from_app_config": "true"
            }
        ],
        "ingestion": [
            {
                "operator": "bash",
                "task_id": "first_task",
                "command": "echo 'This is first task'",
                "dependency": "sequential",
                "load_from_app_config": "true"
            },
            {
                "operator": "bash",
                "task_id": "second_task",
                "command": "echo 'This is second task'",
                "dependency": "sequential",
                "load_from_app_config": "true"
            }
        ]
    }
    dag_id, dag = LoadDags(input_dag).construct_dag()
    task_list = dag.tasks
    assert len(task_list) == 6
