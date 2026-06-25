WITH CTE AS (
    SELECT *,
    LEAD(timestamp, 1) OVER (PARTITION BY machine_id ORDER BY timestamp) AS next_time,
    LEAD(event_type, 1) OVER (PARTITION BY machine_id ORDER BY timestamp) AS next_event
    FROM machine_events
)

SELECT machine_id,
line_id,
station_id,
timestamp AS start_time,
next_time AS stop_time,
TIMESTAMPDIFF(SECOND, timestamp, next_time) AS duration_seconds
FROM CTE
WHERE event_type = 'START'
AND next_event = 'STOP'
AND TIMESTAMPDIFF(SECOND, timestamp, next_time) > 180;
 
WITH CTE AS (
    SELECT *,
    LEAD(event_type, 1) OVER(PARTITION BY machine_id ORDER BY timestamp) AS next_event,
    LEAD(timeStamp, 1) OVER(PARTITION BY machine_id ORDER BY timestamp) AS next_time
    FROM machine_events
)

SELECT machine_id,
line_id,
station_id,
timestamp AS start_time,
next_time AS stop_time,
TIMESTAMPDIFF(SECOND, timestamp, next_time) AS duration_seconds
FROM CTE
WHERE event_type = 'START'
AND next_event = 'STOP'
AND TIMESTAMPDIFF(SECOND, timestamp, next_time) > 180