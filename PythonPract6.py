# Each record contains:
# timestamp, line_id, station_id, vehicle_id, event_type
# event_type = ENTER / EXIT


# A vehicle enters a station with ENTER and leaves the same station with EXIT.
# Return all stations whose average processing time is greater than a given threshold.


from collections import defaultdict
from datetime import datetime

def parse_time(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def average_process_time_analyzer(logs, threshold):
    prev_vehicle_time_map = {}
    total_stations_time_map = defaultdict(int)
    total_stations_count_map = defaultdict(int)
    logs.sort(key=lambda row : row["timestamp"])

    for log in logs:
        vehicle_key = (
            log["line_id"],
            log["station_id"],
            log["vehicle_id"]
        )
        station_key = (
            log["line_id"],
            log["station_id"]
        )

        event = log["event_type"]

        if event == "ENTER":
            prev_vehicle_time_map[vehicle_key] = log
        elif event == "EXIT":
            if vehicle_key not in prev_vehicle_time_map:
                continue
            previous_timestamp = parse_time(prev_vehicle_time_map[vehicle_key]["timestamp"])
            current_timestamp = parse_time(log["timestamp"])
            total_timestamp = (current_timestamp - previous_timestamp).total_seconds()
            total_stations_time_map[station_key] += total_timestamp
            total_stations_count_map[station_key] += 1

            del prev_vehicle_time_map[vehicle_key]
        else:
            continue
    
    result = []
    for k in total_stations_time_map:
        total_time_bystation = total_stations_time_map[k]
        total_count_bystation = total_stations_count_map[k]
        average_process_time_bystation = round(total_time_bystation * 1.0 / total_count_bystation, 2)
        if average_process_time_bystation > threshold:
            result.append({
                "line_id" : k[0],
                "station_id" : k[1],
                "total_time" : total_time_bystation,
                "total_count" :total_count_bystation,
                "avg_process_time" : round(total_time_bystation * 1.0 / total_count_bystation, 2)
            })
    return result

def main():
    logs = [
        {
            "timestamp": "2026-06-22 10:00:00",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "vehicle_id": "VIN001",
            "event_type": "ENTER"
        },
        {
            "timestamp": "2026-06-22 10:04:00",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "vehicle_id": "VIN001",
            "event_type": "EXIT"
        },
        {
            "timestamp": "2026-06-22 10:01:00",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "vehicle_id": "VIN002",
            "event_type": "ENTER"
        },
        {
            "timestamp": "2026-06-22 10:06:30",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "vehicle_id": "VIN002",
            "event_type": "EXIT"
        },
        {
            "timestamp": "2026-06-22 10:02:00",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "vehicle_id": "VIN003",
            "event_type": "ENTER"
        },
        {
            "timestamp": "2026-06-22 10:03:30",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "vehicle_id": "VIN003",
            "event_type": "EXIT"
        },
        {
            "timestamp": "2026-06-22 10:04:00",
            "line_id": "GA5",
            "station_id": "BATTERY_01",
            "vehicle_id": "VIN004",
            "event_type": "EXIT"
        }
    ]

    result = average_process_time_analyzer(
        logs,
        240
    )

    for row in result:
        print(row)

if __name__ == "__main__":
    main()