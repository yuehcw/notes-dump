# Each record contains:
# timestamp, line_id, station_id, vehicle_id, event_type
# event_type = ENTER / EXIT


# A vehicle enters a station with ENTER and leaves the same station with EXIT.
# Return all stations whose average processing time is greater than a given threshold.

from collections import defaultdict 
from datetime import datetime

def parse_date(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def average_process_time_analyzer(logs, threshold):
    logs = sorted(logs, key=lambda log:log["timestamp"])
    active_enter = {}
    total_time = defaultdict(float)
    cycle_count = defaultdict(int)
    
    for log in logs:
        key = (
            log["line_id"],
            log["station_id"],
            log["vehicle_id"]
        )

        station_key = (
            log["line_id"],
            log["station_id"]
        )

        if log["event_type"] == "ENTER":
            active_enter[key] = log
        
        elif log["event_type"] == "EXIT":
            if key not in active_enter:
                continue
            
            enter_time = parse_date(active_enter[key]["timestamp"])
            end_time = parse_date(log["timestamp"])
            interval = (end_time - enter_time).total_seconds()
            total_time[station_key] += interval
            cycle_count[station_key] += 1

            del active_enter[key]

    result = []

    for s in total_time:
        total = total_time[s]
        count = cycle_count[s]
        average = total / count

        if average > threshold:
            result.append({
                "line_id": s[0],
                "station_id": s[1],
                "total": total,
                "count": count,
                "average": round(average, 2)
            })
    
    result.sort(key=lambda row : row["average"], reverse=True)
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