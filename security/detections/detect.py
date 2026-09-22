import json
import sys


def detect_event(log_line):
    try:
        event = json.loads(log_line)
    except json.JSONDecodeError:
        return None

    if event.get("event") == "database_connection_failed":
        return {
            "alert": "DATABASE_CONNECTION_FAILURE",
            "severity": "HIGH",
            "message": "Application failed to connect to the database.",
            "timestamp": event.get("timestamp")
        }

    return None


for line in sys.stdin:
    alert = detect_event(line.strip())

    if alert:
        print(json.dumps(alert))
