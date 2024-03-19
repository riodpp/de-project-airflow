{{ config(engine='MergeTree()', materialized='table') }}

SELECT 
    district,
    city,
    COUNT(id) AS sum_house_sell
FROM {{ ref('fact_house') }}
GROUP BY district, city