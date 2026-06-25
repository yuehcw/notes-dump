# Due to network retries, the same sensor may send multiple readings for the same timestamp. 
# If duplicate readings exist for the same sensor_id and timestamp, keep only the last one in the input list.

# After cleaning the data, return:
# 1. All temperature spike alerts. A spike means the current temperature is more than 20% higher than the previous reading from the same sensor.
# 2. The top k hottest sensors based on average temperature.

from collections import defaultdict
import heapq
def analyze_sensor_data(logs, k):

    # step1 clean the data, only keep the last one for the same sensor_id and timestamp
    cleanhm = {}

    for log in logs:
        sensor_id = log["sensor_id"]
        timestamp = log["timestamp"]
        key = (sensor_id, timestamp)
        cleanhm[key] = log

    clean = list(cleanhm.values())
    clean.sort(key=lambda row : (row["sensor_id"], row["timestamp"]))    

    # step2 allocation the spike alert data

    alert = []
    prev_temp_dict = {}
    for c in clean:
        sensor_id = c["sensor_id"]
        if sensor_id in prev_temp_dict:
            prev_temp = prev_temp_dict[sensor_id]["temperature"]
            cur_temperature = c["temperature"]


            if cur_temperature > prev_temp * 1.2:
                alert.append({
                    "sensor_id" : sensor_id,
                    "timestamp" : c["timestamp"],
                    "prevtimestamp" : prev_temp_dict[sensor_id]["timestamp"],
                    "temperature" : cur_temperature,
                    "increase_percentage" : round((cur_temperature - prev_temp) / prev_temp * 100,2)
                })

        prev_temp_dict[sensor_id] = c
    
    # step3 The top k hottest sensors based on average temperature
    sensor_temp = defaultdict(float)
    sensor_count = defaultdict(int)

    for c in clean:
        sensor_id = c["sensor_id"]
        sensor_temp[sensor_id] += c["temperature"]
        sensor_count[sensor_id] += 1
    
    avg_temps = []

    for id in sensor_temp:
        avg = sensor_temp[id] / sensor_count[id]
        heapq.heappush(avg_temps, (avg, id))

        if len(avg_temps) > k:
            heapq.heappop(avg_temps)
    
    return alert, avg_temps
    

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
