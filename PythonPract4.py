# Return all stations whose failure rate is greater than a given threshold.
# Each record contains:
# timestamp, line_id, station_id, vehicle_id, inspection_type, result
# result = PASS / FAIL


# Failure rate is defined as:
# fail_count / total_inspection_count

from collections import defaultdict
def failure_rate_analyzer(logs, threshold):
    total_count_map = defaultdict(int)
    fail_count_map = defaultdict(int)
    result = []

    for log in logs:
        key = (
            log["line_id"],
            log["station_id"]
        )

        result_type = log["result"]
        if result_type == "FAIL":
            fail_count_map[key] += 1
        total_count_map[key] += 1
    
    for k in total_count_map:
        fail_rate = round(fail_count_map[k] * 1.0 / total_count_map[k],2)
        if fail_rate > threshold:
            result.append({
                "line_id" : k[0],
                "station_id" : k[1],
                "total_inspection" : total_count_map[k],
                "failed_inspection" : fail_count_map[k],
                "fail_rate" : fail_rate
            })

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