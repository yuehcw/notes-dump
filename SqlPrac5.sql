WITH CTE AS (
    SELECT *,
    AVG(temperature) OVER(PARTITION BY sensor_id ORDER BY timestamp ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_avg_temperature,
    COUNT(*) OVER(PARTITION BY sensor_id ORDER BY timestamp ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS window_count
    FROM sensor_readings
)

SELECT sensor_id,
line_id,
station_id,
timestamp,
temperature,
rolling_avg_temperature
FROM CTE
WHERE rolling_avg_temperature > 80
AND window_count = 3;
