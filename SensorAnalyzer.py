# Due to network retries, the same sensor may send multiple readings for the same timestamp. 
# If duplicate readings exist for the same sensor_id and timestamp, keep only the last one in the input list.

# After cleaning the data, return:
# 1. All temperature spike alerts. A spike means the current temperature is more than 20% higher than the previous reading from the same sensor.
# 2. The top k hottest sensors based on average temperature.

from collections import defaultdict
import heapq
class SensorAnalyzer:
    def __init__(self, logs):
        self.logs = logs
    
    def clean_logs(self):
        latest = {}

        for log in self.logs:
            key = (log["sensor_id"], log["timestamp"])
            latest[key] = log
        
        cleaned = list(latest.values())
        cleaned.sort(key=lambda log: (log["sensor_id"], log["timestamp"]))

        return cleaned
    
    def detect_spikes(self, cleaned_logs):
        prev_temp = {}
        alerts = []

        for log in cleaned_logs:
            sensor_id = log["sensor_id"]
            temp = log["temperature"]

            if sensor_id in prev_temp:
                prev = prev_temp[sensor_id]

                if temp > prev * 1.2:
                    alerts.append({
                        "timestamp": log["timestamp"],
                        "line_id": log["line_id"],
                        "station_id": log["station_id"],
                        "sensor_id": sensor_id,
                        "prev_temp": prev,
                        "current_temp": temp,
                        "increase_percent": round((temp - prev) / prev * 100,2)  
                    })

            prev_temp[sensor_id] = temp
            
        return alerts
       
    
    def top_k_hottest_sensors(self, cleaned_logs, k):
        temp_sum = defaultdict(float)
        temp_count = defaultdict(int)
       
        for log in cleaned_logs:
            sensor_id = log["sensor_id"]
            temp_sum[sensor_id] += log["temperature"]
            temp_count[sensor_id] += 1
        
        avg_temps = []

        for sensor_id in temp_sum:
            avg = temp_sum[sensor_id] / temp_count[sensor_id]
            heapq.heappush(avg_temps, (avg, sensor_id))

            if len(avg_temps) > k:
                heapq.heappop(avg_temps)
        
        return avg_temps
    
    def analyze(self, k):
        cleaned_logs = self.clean_logs()
        alerts = self.detect_spikes(cleaned_logs)
        top_k_sensors = self.top_k_hottest_sensors(cleaned_logs, k)

        return {
            "alerts": alerts,
            "top_k_sensors": top_k_sensors
        }

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

    analyzer = SensorAnalyzer(sensor_logs)
    result = analyzer.analyze(k=2)
    print("Spike Alerts:")
    for alert in result["alerts"]:
        print(alert)
    
    print("\nTop K Hottest Sensors:")
    for avg_temp, sensor_id in result["top_k_sensors"]:
        print(f"Sensor ID: {sensor_id}, Average Temperature: {avg_temp :.2f}")

if __name__ == "__main__":
    main()