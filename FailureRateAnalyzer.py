# Return all stations whose failure rate is greater than a given threshold.
# Each record contains:
# timestamp, line_id, station_id, vehicle_id, inspection_type, result
# result = PASS / FAIL


# Failure rate is defined as:
# fail_count / total_inspection_count

from collections import defaultdict
def failure_rate_analyzer(logs, threshold):
    total_count = defaultdict(int)
    failure_count = defaultdict(int)

    for log in logs:
        inspection_result = log["result"]
        key = (
            log["line_id"],
            log["station_id"]
        )

        total_count[key] += 1
        if inspection_result == "FAIL":
            failure_count[key] += 1
    
    result =[]

    for k in total_count:
        total = total_count[k]
        failure = failure_count[k]
        failure_rate = round(failure / total, 2)
        if failure_rate > threshold:
            result.append({
                "line_id" : k[0],
                "station_id" : k[1],
                "total_count" : total,
                "fail_count" : failure,
                "failure_rate" : failure_rate
            }) 
    
    result = sorted(result, key=lambda row : row["failure_rate"], reverse=True)
    return result

def main():
    logs = [
        {
            "timestamp": "2026-06-22 10:00:01",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "vehicle_id": "VIN001",
            "inspection_type": "weld_strength",
            "result": "PASS"
        },
        {
            "timestamp": "2026-06-22 10:01:10",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "vehicle_id": "VIN002",
            "inspection_type": "weld_strength",
            "result": "FAIL"
        },
        {
            "timestamp": "2026-06-22 10:02:20",
            "line_id": "GA4",
            "station_id": "WELD_01",
            "vehicle_id": "VIN003",
            "inspection_type": "weld_strength",
            "result": "FAIL"
        },
        {
            "timestamp": "2026-06-22 10:00:05",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "vehicle_id": "VIN004",
            "inspection_type": "paint_defect",
            "result": "PASS"
        },
        {
            "timestamp": "2026-06-22 10:01:15",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "vehicle_id": "VIN005",
            "inspection_type": "paint_defect",
            "result": "PASS"
        },
        {
            "timestamp": "2026-06-22 10:02:25",
            "line_id": "GA4",
            "station_id": "PAINT_02",
            "vehicle_id": "VIN006",
            "inspection_type": "paint_defect",
            "result": "FAIL"
        },
        {
            "timestamp": "2026-06-22 10:03:00",
            "line_id": "GA5",
            "station_id": "BATTERY_01",
            "vehicle_id": "VIN007",
            "inspection_type": "voltage_check",
            "result": "FAIL"
        },
        {
            "timestamp": "2026-06-22 10:04:00",
            "line_id": "GA5",
            "station_id": "BATTERY_01",
            "vehicle_id": "VIN008",
            "inspection_type": "voltage_check",
            "result": "FAIL"
        },
        {
            "timestamp": "2026-06-22 10:05:00",
            "line_id": "GA5",
            "station_id": "BATTERY_01",
            "vehicle_id": "VIN009",
            "inspection_type": "voltage_check",
            "result": "PASS"
        }
    ]

    result = failure_rate_analyzer(logs, 0.5)
    for row in result:
        print(row)

if __name__ == "__main__":
    main()