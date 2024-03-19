from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from pendulum import datetime


@dag(start_date=datetime(2022, 8, 1), schedule=None, catchup=False)
def bash_two_commands_example_dag():
    scrape_data = BashOperator(
        task_id="scrape_data_website",
        bash_command="echo $AIRFLOW_HOME"
    )

    try_docker_operator = DockerOperator(
        task_id='run_docker_container_test',
        image='python:3.10-slim-bullseye',
        command='python --version',
        container_name='coba-docker-operator-1',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        mount_tmp_dir=False,
        auto_remove='success'
    )

    try_docker_operator = DockerOperator(
        task_id='extract_mongo',
        image='extract-mongo:1.0',
        command=["python", "extract_mongo_clickhouse.py"],
        container_name='extract-mongo',
        docker_url='unix://var/run/docker.sock',
        network_mode='data-eng-network',
        mount_tmp_dir=False,
        auto_remove='success',
        environment={
            'CLICKHOUSE_HOST': 'clickhousedb',
            'CLICKHOUSE_USER': 'default_user',
            'CLICKHOUSE_PASSWORD': 'default_password',
            'MONGO_HOST': 'mongodb',
            'MONGO_USER': 'user',
            'MONGO_PASSWORD': 'password'
        }
    )

    try_dbt_clickhouse = DockerOperator(
        task_id='run_dbt_clickhouse',
        image='dbt-clickhouse-custom:1.0',
        command=["run", "--models", "my_second_dbt_model"],
        container_name='coba-dbt-clickhouse',
        docker_url='unix://var/run/docker.sock',
        network_mode='data-eng-network',
        mount_tmp_dir=False,
        auto_remove='success',
        environment={
            'HOST_CLICKHOUSE': 'clickhousedb'
        }
        
    )

    scrape_data >> try_docker_operator >> try_dbt_clickhouse


bash_two_commands_example_dag()