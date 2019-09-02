from functools import reduce

import airflow
from airflow.models import DAG
from airflow.utils import helpers
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator

from essentials.support import Support


class LoadDags():
    def __init__(self, dag_attribute):
        self.dag_attribute = dag_attribute

    def construct_dag(self):
        dag_id = self.dag_attribute['dag_id']
        default_args = {
            'owner': 'data_engineering_team',
            'start_date': airflow.utils.dates.days_ago(2),
            'depends_on_past': False,
            'email_on_failure': False,
            'email_on_retry': False
        }
        dag = DAG(dag_id,
                  schedule_interval=None,
                  default_args=default_args)

        groups = Support().supported_groups()
        dag_groups = []
        for k, group in enumerate(groups):
            if group in self.dag_attribute:
                dag_groups.append(self.construct_one_group(self.dag_attribute[group], group, dag))
        # reduce(lambda group1, group2: group1[1] >> group2[0], dag_groups)
        # helpers.chain(dag_groups)
        for k,group in enumerate(dag_groups):
            if k < len(dag_groups) - 1:
                group[1].set_downstream(dag_groups[k + 1][0])

        # helpers.cross_downstream(dag_groups[0], dag_groups[1])
        # from_tasks = dag_groups[0]
        # to_tasks = dag_groups[1]
        # for task in from_tasks:
        #     task.set_downstream(to_tasks)
        return (dag_id, dag)

    def construct_one_group(self, task_list, group_name, dag):
        """
        This function constructs all the task of one group
        :param task_list: list
        :param group_name: str
        :param dag: DAG object
        :return: List[Airflow Operators]
        """
        grp_actual_task = []
        for each_task in task_list:
            grp_actual_task.append(self.construct_task(each_task, group_name, dag))

        sequential = True
        if sequential:
            length = len(grp_actual_task)
            if length > 0:
                first_task = grp_actual_task[0]
                last_task = grp_actual_task[length - 1]
                reduce(lambda first, second: first >> second, grp_actual_task)
                return first_task, last_task  # reduce(lambda first, second: first >> second, grp_actual_task)
        else:
            return grp_actual_task

    def _load_function_args_from_config(self):
        pass

    def construct_task(self, task_details, group_name, dag):
        """
        Constructs the individual task based on the task_details provided
        :param task_details: dict
        :param group_name: str
        :param dag: DAG object
        :return: Airflow Operator
        """
        operator_type = task_details['operator']
        load_from_config = True if task_details['load_from_app_config'] == 'true' else False
        task_id = '_'.join([group_name, task_details['task_id']])
        if operator_type == 'bash':
            return BashOperator(
                task_id=task_id,
                bash_command=task_details['command'],
                dag=dag
            )
        elif operator_type == 'python':
            return PythonOperator(
                task_id=task_id,
                python_callable=eval(task_details['function_name']),
                op_kwargs=task_details['function_kwargs'],
                provide_context=True,
                dag=dag
            )
        elif operator_type == 'ssh':
            return SSHOperator(
                task_id=task_id,
                ssh_conn_id=task_details['conn_id'],
                command=task_details['command'],
                dag=dag
            )
        elif operator_type == 'postgres':
            return PostgresOperator(
                task_id=task_id,
                postgres_conn_id=task_details['conn_id'],
                sql=task_details['sql'],
                dag=dag
            )
        elif operator_type == 'branch_python':
            return BranchPythonOperator(
                task_id=task_id,
                python_callable=eval(task_details['function_name']),
                op_kwargs=task_details['function_kwargs'],
                provide_context=True,
                dag=dag
            )
        else:
            return DummyOperator(
                task_id=task_id,
                dag=dag
            )
