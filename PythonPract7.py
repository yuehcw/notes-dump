def status_analyzer(logs):
    distinct_map = {}
    for log in logs:
        key = (
            log["machine_id"],
            log["timestamp"],
            log["status"]
        )
        distinct_map[key] = log
    clean = list(distinct_map.values())
    clean.sort(key=lambda row : (row["machine_id"], row["timestamp"]))

    prev_log = {}
    result = []
    for row in clean:
        machine_id = row["machine_id"]
        status = row["status"]

        if machine_id in prev_log:
            prev_status = prev_log[machine_id]["status"]

            if prev_status == "RUNNING" and status == "ERROR":
                result.append({
                    "machine_id" : machine_id,
                    "line_id" : row["line_id"],
                    "station_id" : row["station_id"],
                    "error_timestamp" : row["timestamp"],
                    "previous_status" : prev_status,
                    "current_status" : status
                })
                
        prev_log[machine_id] = row
    return result
    