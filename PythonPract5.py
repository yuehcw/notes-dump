# A machine cycle starts with START and ends with the next STOP from the same machine_id.
# Return all machines whose cycle duration is greater than a given threshold.

from datetime import datetime
def parse_time(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def find_slow_cycles(logs, threshold):
    logs.sort(key=lambda row : row["timestamp"])
    # 先sort, 題目不保證是按照時間順序來的 

    prev_record_map = {}
    result = []

    for log in logs:
        key = (
            log["line_id"],
            log["station_id"],
            log["machine_id"]
        )
        event = log["event_type"]
        if event == "START":
            prev_record_map[key] = log
        
        elif event == "STOP":
            if key not in prev_record_map:
                continue
            previous_time = parse_time(prev_record_map[key]["timestamp"])
            current_time = parse_time(log["timestamp"])
            time_duration = (current_time - previous_time).total_seconds()

            if time_duration > threshold:
                result.append({
                    "line_id" : log["line_id"],
                    "station_id" : log["station_id"],
                    "machine_id" : log["machine_id"],
                    "previous_timestamp" : prev_record_map[key]["timestamp"],
                    "current_timestamp" : log["timestamp"],
                    "time_duration" : time_duration,
                    "exceeded_time" : time_duration - threshold
                })
            del prev_record_map[key]
            # 避免被重複的STOP用到
        else:
            continue
    return result



def main():
    logs = [
        {
            "timestamp": "2026-06-22 10:00:00",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "machine_id": "ROBOT_001",
            "event_type": "START"
        },
        {
            "timestamp": "2026-06-22 10:02:30",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "machine_id": "ROBOT_001",
            "event_type": "STOP"
        },
        {
            "timestamp": "2026-06-22 10:00:10",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "machine_id": "ROBOT_002",
            "event_type": "START"
        },
        {
            "timestamp": "2026-06-22 10:06:00",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "machine_id": "ROBOT_002",
            "event_type": "STOP"
        },
        {
            "timestamp": "2026-06-22 10:01:00",
            "line_id": "GA5",
            "station_id": "BATTERY_01",
            "machine_id": "ROBOT_003",
            "event_type": "STOP"
        }
    ]

    result = find_slow_cycles(logs, 180)
    print(result)

if __name__ == "__main__":
    main()