# A sensor is considered unstable if, within any 3 consecutive readings from the same sensor, 
# the temperature range is greater than a given threshold.
# Temperature range: (max_temperature - min_temperature)
# Return all unstable windows.

from collections import defaultdict, deque
def find_unstable_window(logs, window_size, range_threshold):
    logs.sort(key=lambda row : (row["sensor_id"],row["timestamp"]))
    sensor_window = defaultdict(deque)
    sensor_window_temp = defaultdict(deque)
    result = []

    for log in logs:
        sensor_id = log["sensor_id"]
        sensor_window[sensor_id].append(log)
        sensor_window_temp[sensor_id].append(log["temperature"])

        if len(sensor_window[sensor_id]) > window_size:
            sensor_window[sensor_id].popleft()
            sensor_window_temp[sensor_id].popleft()

        if len(sensor_window[sensor_id]) == window_size:
            max_temp = max(sensor_window_temp[sensor_id])
            min_temp = min(sensor_window_temp[sensor_id])

            if max_temp - min_temp > range_threshold:
                result.append({
                    "sensor_id" : sensor_id,
                    "start_time" : sensor_window[sensor_id][0]["timestamp"],
                    "end_time" : log["timestamp"],
                    "temperature_range": max_temp - min_temp
                })
    return result



def main():
    logs = [
        {
            "timestamp": "2026-06-22 10:00:01",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "sensor_id": "TEMP_001",
            "temperature": 71.5
        },
        {
            "timestamp": "2026-06-22 10:00:02",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "sensor_id": "TEMP_001",
            "temperature": 72.0
        },
        {
            "timestamp": "2026-06-22 10:00:03",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "sensor_id": "TEMP_001",
            "temperature": 86.8
        },
        {
            "timestamp": "2026-06-22 10:00:04",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "sensor_id": "TEMP_001",
            "temperature": 73.0
        },
        {
            "timestamp": "2026-06-22 10:00:01",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "sensor_id": "TEMP_002",
            "temperature": 55.0
        },
        {
            "timestamp": "2026-06-22 10:00:02",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "sensor_id": "TEMP_002",
            "temperature": 56.1
        },
        {
            "timestamp": "2026-06-22 10:00:03",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "sensor_id": "TEMP_002",
            "temperature": 57.0
        },
        {
            "timestamp": "2026-06-22 10:00:01",
            "line_id": "GA5",
            "station_id": "BATTERY_01",
            "sensor_id": "TEMP_003",
            "temperature": 88.0
        },
        {
            "timestamp": "2026-06-22 10:00:02",
            "line_id": "GA5",
            "station_id": "BATTERY_01",
            "sensor_id": "TEMP_003",
            "temperature": 89.0
        },
        {
            "timestamp": "2026-06-22 10:00:03",
            "line_id": "GA5",
            "station_id": "BATTERY_01",
            "sensor_id": "TEMP_003",
            "temperature": 91.0
        }
    ]

    result = find_unstable_window(logs, 3, 10)
    print(result)

if __name__ == "__main__":
    main()