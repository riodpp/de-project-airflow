from pymongo import MongoClient
from clickhouse_driver import Client
from datetime import datetime

import os

# Connect to MongoDB
mongo_client = MongoClient('mongodb://' + os.environ['MONGO_USER'] + ':' + os.environ['MONGO_PASSWORD'] + '@' + os.environ['MONGO_HOST'] + ':27017/')
mongo_db = mongo_client['olx_house']
mongo_collection = mongo_db['houses']

# Connect to ClickHouse
ch_client = Client(host=os.environ['CLICKHOUSE_HOST'], user=os.environ['CLICKHOUSE_USER'], password=os.environ['CLICKHOUSE_PASSWORD'], database='de_project')

# Delete the table in ClickHouse
ch_client.execute('''
    DROP TABLE IF EXISTS houses_raw
''')

# Create a table in ClickHouse
ch_client.execute('''
    CREATE TABLE IF NOT EXISTS houses_raw (
        id String,
        price Decimal(10,2),
        bedroom Int8,
        bathroom Int8,
        area Int32,
        district String,
        city String,
        release_date Date
    ) ENGINE = MergeTree()
    ORDER BY id
''')

# Extract data from MongoDB
mongo_data = mongo_collection.find()

# Load data into ClickHouse
for document in mongo_data:
    release_date = datetime.strptime(document['releaseDate'], '%Y/%m/%d')
    ch_client.execute('INSERT INTO houses_raw VALUES', [(
        str(document['id']),
        document['price'],
        document['bedroom'],
        document['bathroom'],
        document['area'],
        document['district'],
        document['city'],
        release_date
    )])