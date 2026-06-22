# A machine cycle starts with START and ends with the next STOP from the same machine_id.
# Return all machines whose cycle duration is greater than a given threshold.


from datetime import datetime
def parse_time(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def find_slow_cycles(logs, threshold):
    active_start = {}
    slow_machine = []

    logs = sorted(logs, key=lambda log:log["timestamp"])

    for log in logs:
        machine_id = log["machine_id"]
        event_type = log["event_type"]
        if event_type == "START":
            active_start[machine_id] = log
        
        elif event_type == "STOP":
            if machine_id not in active_start:
                continue
            
            start_time = parse_time(active_start[machine_id]["timestamp"])
            stop_time = parse_time(log["timestamp"])
            interval_time = (stop_time - start_time).total_seconds()

            if interval_time > threshold:
                slow_machine.append({
                    "machine_id" : machine_id,
                    "line_id" : log["line_id"],
                    "station_id" : log["station_id"],
                    "start_time" : active_start[machine_id]["timestamp"],
                    "stop_time" : log["timestamp"],
                    "duration_seconds" : int(interval_time)
                })
            del active_start[machine_id]
    return slow_machine

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