WITH CTE AS (
    SELECT 
        line_id,
        station_id,
        COUNT(*) AS total_count,
        SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END) AS fail_count
    FROM quality_inspections
    GROUP BY line_id, station_id
),
CLEAN AS (
    SELECT 
        line_id,
        station_id,
        total_count AS total_inspections,
        fail_count AS failed_inspections,
        ROUND(fail_count * 1.0 / total_count,2) AS failure_rate,
        DENSE_RANK() OVER(ORDER BY fail_count * 1.0 / total_count DESC) AS rk
    FROM CTE
    WHERE total_inspections >= 5
)

SELECT line_id,
station_id,
total_inspections,
failed_inspections,
failure_rate
FROM CLEAN
WHERE rk <= 3;







WITH CTE AS (
    SELECT line_id,
    station_id,
    COUNT(inspection_id) AS total_count,
    SUM(CASE WHEN result = 'FAIL' THEN 1 ELSE 0 END) AS total_fail_count
    FROM quality_inspections
    GROUP BY line_id, station_id
),
CTE2 AS (
    SELECT *,
    ROUND(total_fail_count * 1.0 / total_count,2) AS failure_rate
    -- 整數/整數 = 整數. EX: 2/5 = 0
    FROM CTE
    WHERE total_count >= 5
),
CTE3 AS (
    SELECT *,
    DENSE_RANK() OVER(ORDER BY failure_rate DESC) AS rk
    FROM CTE2
)

SELECT line_id,
station_id,
total_count AS total_inspections,
total_fail_count AS failed_inspections,
failure_rate,
rk AS rank 
FROM CTE3
WHERE rk <= 3





