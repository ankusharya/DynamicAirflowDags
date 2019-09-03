class LoadJSON():
    def __init__(self):
        pass

    def load_json_dict(self):
        input_dags = [
            {
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
            },
            {
                "dag_id": "dynamic_trigger_test_2",
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
        ]
        return input_dags
