FROM python:3.10-slim-bullseye

RUN apt-get update && apt-get install -y curl
RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["dbt"]