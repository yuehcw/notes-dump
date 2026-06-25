# A healthy sensor should report once every minute.

# Return all sensors that missed at least one expected heartbeat 
# between their first and last observed timestamp.

# Assume timestamps are already rounded to the minute.

from collections import defaultdict
from datetime import datetime

def parse_time(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def find_missing_heartbeats(logs):
    sensor_map = defaultdict(list)
    result = []

    for log in logs:
        key = (
            log["line_id"],
            log["station_id"],
            log["machine_id"],
            log["sensor_id"]
        )
        sensor_map[key].append(log)

    for k, v in sensor_map.items():
        v.sort(key=lambda row : row["timestamp"])

        for i in range(1, len(v)):
            prev_timestamp = parse_time(v[i-1]["timestamp"])
            cur_timestamp = parse_time(v[i]["timestamp"])
            time_gap = (cur_timestamp - prev_timestamp).total_seconds() // 60
            if time_gap > 1:
                result.append({
                    "line_id" : k[0],
                    "station_id" : k[1],
                    "machine_id" : k[2],
                    "start_time" : v[i-1]["timestamp"],
                    "stop_time" : v[i]["timestamp"],
                    "miss_count" : int(time_gap - 1)
                })
    return result

def main():
    logs = [
        {
            "timestamp": "2026-06-22 10:00:00",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "machine_id": "ROBOT_001",
            "sensor_id": "TEMP_001",
            "status": "OK"
        },
        {
            "timestamp": "2026-06-22 10:01:00",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "machine_id": "ROBOT_001",
            "sensor_id": "TEMP_001",
            "status": "OK"
        },
        {
            "timestamp": "2026-06-22 10:04:00",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "machine_id": "ROBOT_001",
            "sensor_id": "TEMP_001",
            "status": "OK"
        },
        {
            "timestamp": "2026-06-22 10:00:00",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "machine_id": "ROBOT_002",
            "sensor_id": "PRESSURE_001",
            "status": "OK"
        },
        {
            "timestamp": "2026-06-22 10:01:00",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "machine_id": "ROBOT_002",
            "sensor_id": "PRESSURE_001",
            "status": "OK"
        },
        {
            "timestamp": "2026-06-22 10:02:00",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "machine_id": "ROBOT_002",
            "sensor_id": "PRESSURE_001",
            "status": "OK"
        }
    ]

    result = find_missing_heartbeats(logs)

    for row in result:
        print(row)

if __name__ == "__main__":
    main()