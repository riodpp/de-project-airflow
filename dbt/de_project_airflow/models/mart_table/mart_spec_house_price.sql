{{ config(engine='MergeTree()', materialized='table') }}

SELECT 
    district,
    city,
    CASE
        WHEN area < 50 THEN '< 50'
        WHEN area BETWEEN 50 AND 100 THEN '50-100'
        WHEN area BETWEEN 100 AND 200 THEN '100-200'
        WHEN area BETWEEN 200 AND 300 THEN '200-300'
        ELSE '> 300'
    END AS area_group,
    AVG(price) AS avg_house_price,
    MIN(price) AS min_house_price,
    MAX(price) AS max_house_price
FROM {{ ref('fact_house') }}
GROUP BY 1,2,3
ORDER BY 2,1,3