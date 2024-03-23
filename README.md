# Description
This project is made for exploration about DockerOperator in Airflow.

# Requirements
- Docker
- Astronomer CLI
- dbt-clickhouse
- Pyenv (Optional)

# How To Setup
Each folder is consisting all of services needed to run the entire project. 
First create virtual environment using Pyenv or virtualenv. 
- Pyenv
```
pyenv virtualenv 3.10 sandbox
```
to create vurtual env named sandbox.

## DB services
This project will using mongodb as temporary storage from scraping data and clickhouse as datawarehouse.
To setup these db we need to run the services using docker-compose.
```
docker compose up -d
```
We also provide dump json to try the project `houses.json`. Import your data using mongosh or MongoDB Compass.

## Airflow
Here we are using astronomer to create and running airflow instance.
```
airflow dev start
```
This command will creating all container needed to run airflow. 

## DBT
Create image for DBT using below command
```
docker build -t dbt-clickhouse-custom:1.0 .
```
This will creating image in your local docker. Later this image will be called by airflow.

## Script Python
Same as DBT, create image for python script for extracting mongodb data and load the data to clickhouse
```
docker build -t mongo-extract:1.0 .
```

# How to run
After all the services was running. You can visit localhost:8080 to open Airflow UI. Choose the DAg and run the task. That's it



