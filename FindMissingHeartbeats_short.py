# A healthy sensor should report once every minute.

# Return all sensors that missed at least one expected heartbeat 
# between their first and last observed timestamp.

# Assume timestamps are already rounded to the minute.

from collections import defaultdict
from datetime import datetime

def parse_time(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


def find_missing_heartbeats(logs):
    by_sensor = defaultdict(list)
    
    for log in logs:
        key = (
            log["line_id"],
            log["station_id"],
            log["machine_id"],
            log["sensor_id"]
        )
        by_sensor[key].append(log)
    
    result = []
    for k, v in by_sensor.items():
        v = sorted(v, key=lambda log:log["timestamp"])

        for i in range(1, len(v)):
            prev_time = parse_time(v[i - 1]["timestamp"])
            curr_time = parse_time(v[i]["timestamp"])

            diff_minutes = int((curr_time - prev_time).total_seconds() // 60)

            if diff_minutes > 1:
                result.append({
                    "line_id": k[0],
                    "station_id": k[1],
                    "machine_id": k[2],
                    "sensor_id": k[3],
                    "last_seen": v[i - 1]["timestamp"],
                    "next_seen": v[i]["timestamp"],
                    "missed_count": diff_minutes - 1
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