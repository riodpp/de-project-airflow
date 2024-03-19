{{ config(order_by='(updated_at, id)', engine='MergeTree()', materialized='table') }}

SELECT 
    DISTINCT *,
    release_date AS updated_at
FROM {{ source('lake', 'houses_raw') }}