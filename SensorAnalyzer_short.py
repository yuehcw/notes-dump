# Due to network retries, the same sensor may send multiple readings for the same timestamp. 
# If duplicate readings exist for the same sensor_id and timestamp, keep only the last one in the input list.

# After cleaning the data, return:
# 1. All temperature spike alerts. A spike means the current temperature is more than 20% higher than the previous reading from the same sensor.
# 2. The top k hottest sensors based on average temperature.

from collections import defaultdict
import heapq

def analyze_sensor_data(logs, k):

    # Step 1: Clean the logs
    cleaned = {}
    for log in logs:
        sensor_id = log["sensor_id"]
        timestamp = log["timestamp"]
        cleaned[(sensor_id, timestamp)] = log
    
    cleaned = list(cleaned.values())
    cleaned.sort(key=lambda log : (log["sensor_id"], log["timestamp"]))

    # Step 2: Find the spike machine
    prev_temp = {}
    alerts = []

    for log in cleaned:
        sensor_id = log["sensor_id"]
        temp = log["temperature"]

        if sensor_id in prev_temp:
            prev = prev_temp[sensor_id]

            if temp > prev * 1.2:
                alerts.append(
                    {
                        "timestamp":log["timestamp"],
                        "sensor_id":sensor_id,
                        "line_id":log["line_id"],
                        "station_id":log["station_id"],
                        "temperature":temp,
                        "percent_increase": (temp - prev) / prev * 100
                    }
                )
        prev_temp[sensor_id] = temp
    
    #Step 3: Find the top k hottest sensors based on avgerage temperature
    sensor_temp = defaultdict(float)
    sensor_count = defaultdict(int)

    for log in cleaned:
        sensor_id = log["sensor_id"]
        temp = log["temperature"]
        sensor_temp[sensor_id] += temp
        sensor_count[sensor_id] += 1

    avg_temps = []
    for sensor_id in sensor_temp:
        avg = sensor_temp[sensor_id] / sensor_count[sensor_id]
        heapq.heappush(avg_temps, (avg, sensor_id))

        if len(avg_temps) > k:
            heapq.heappop(avg_temps)
    
    return alerts, avg_temps

def main():
    sensor_logs = [
        {
            "timestamp": "2026-06-22 10:00:01",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "sensor_id": "TEMP_001",
            "temperature": 72.0
        },
        {
            "timestamp": "2026-06-22 10:00:01",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "sensor_id": "TEMP_001",
            "temperature": 73.0
        },
        {
            "timestamp": "2026-06-22 10:00:02",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "sensor_id": "TEMP_001",
            "temperature": 75.0
        },
        {
            "timestamp": "2026-06-22 10:00:03",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "sensor_id": "TEMP_001",
            "temperature": 95.0
        },
        {
            "timestamp": "2026-06-22 10:00:01",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "sensor_id": "TEMP_002",
            "temperature": 40.0
        },
        {
            "timestamp": "2026-06-22 10:00:02",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "sensor_id": "TEMP_002",
            "temperature": 41.0
        },
        {
            "timestamp": "2026-06-22 10:00:03",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "sensor_id": "TEMP_002",
            "temperature": 60.0
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
        }
    ]

    alerts, avg_temps = analyze_sensor_data(sensor_logs, 2)
    print(alerts)
    print("-------------------")
    print(avg_temps)

if __name__ == "__main__":
    main()
