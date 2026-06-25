WITH CTE AS (
    SELECT *,
    ROW_NUMBER() OVER(PARTITION BY sensor_id, timestamp ORDER BY reading_id DESC) AS rw
    FROM sensor_readings
), 
CTE2 AS (
    SELECT *,
    LAG(temperature, 1) OVER(PARTITION BY sensor_id ORDER BY timestamp) AS previous_temp
    FROM CTE
    WHERE rw = 1
)

SELECT sensor_id,
line_id,
station_id,
timestamp,
previous_temp AS previous_temperature,
temperature AS current_temperature,
ROUND((temperature - previous_temp) / previous_temp * 100,2) AS increase_percent
FROM CTE2
WHERE temperature > previous_temp * 1.2;



WITH CTE AS (
    SELECT *
    , ROW_NUMBER() OVER(PARTITION BY sensor_id, timestamp ORDER BY reading_id DESC) AS rw
    FROM sensor_readings
),
CLEAN AS (
    SELECT *
    , LAG(temperature, 1) OVER(PARTITION BY sensor_id ORDER BY timestamp) AS previous_temperature
    FROM CTE
    WHERE rw = 1
)
SELECT sensor_id,
line_id,
station_id,
timestamp,
previous_temperature,
temperature AS current_temperature,
ROUND((temperature - previous_temperature) / previous_temperature * 100,2) AS increase_percent
FROM CLEAN
WHERE temperature > previous_temperature * 1.2