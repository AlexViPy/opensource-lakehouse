{{ config(
        pre_hook="CREATE DATABASE IF NOT EXISTS silver"
	)
}}


SELECT
    Team
    ,COUNT(*) AS PlayersCount
FROM {{ source("fifa_wc", "fifa") }}