WITH CTE AS (
    SELECT *,
    LAG(temperature, 1) OVER(PARTITION BY sensor_id ORDER BY timestamp) AS previous_temp
    FROM sensor_readings
),
CTE2 AS (
    SELECT *,
    temperature - previous_temp AS temperature_difference
    FROM CTE
)

SELECT sensor_id,
line_id,
station_id,
timestamp,
previous_temp AS previous_temperature,
temperature AS current_temperature,
temperature_difference
FROM CTE2
WHERE temperature_difference >= 15