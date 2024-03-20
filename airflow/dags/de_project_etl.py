from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from pendulum import datetime


@dag(start_date=datetime(2022, 8, 1), schedule=None, catchup=False)
def airflow_docker_operator():

    extract_mongo_task = DockerOperator(
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

    fact_house_task = DockerOperator(
        task_id='fact_house',
        image='dbt-clickhouse-custom:1.0',
        command=["run", "--models", "fact_house"],
        container_name='fact-house',
        docker_url='unix://var/run/docker.sock',
        network_mode='data-eng-network',
        mount_tmp_dir=False,
        auto_remove='success',
        environment={
            'HOST_CLICKHOUSE': 'clickhousedb'
        }   
    )

    mart_region_house_sell_task = DockerOperator(
        task_id='mart_region_house_sell',
        image='dbt-clickhouse-custom:1.0',
        command=["run", "--models", "mart_region_house_sell"],
        container_name='mart-region-house-sell',
        docker_url='unix://var/run/docker.sock',
        network_mode='data-eng-network',
        mount_tmp_dir=False,
        auto_remove='success',
        environment={
            'HOST_CLICKHOUSE': 'clickhousedb'
        }   
    )

    mart_spec_house_price_task = DockerOperator(
        task_id='mart_spec_house_price',
        image='dbt-clickhouse-custom:1.0',
        command=["run", "--models", "mart_spec_house_price"],
        container_name='mart_spec_house_price',
        docker_url='unix://var/run/docker.sock',
        network_mode='data-eng-network',
        mount_tmp_dir=False,
        auto_remove='success',
        environment={
            'HOST_CLICKHOUSE': 'clickhousedb'
        }   
    )

    extract_mongo_task >> fact_house_task >> mart_region_house_sell_task
    fact_house_task >> mart_spec_house_price_task


airflow_docker_operator()