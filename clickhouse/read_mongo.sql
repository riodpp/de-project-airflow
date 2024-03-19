CREATE TABLE IF NOT EXISTS deproject.house_data
(
    id String,
    price Decimal(10,2),
    bedroom Int8,
    bathroom Int8,
    area Int8,
    district String,
    city String,
    releaseDate Date,
    url String
)
ENGINE = MongoDB('de-project-airflow-mongodb-1:27017', 'olx_house', 'house', 'user', 'password');