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

    if event.get("event") == "authentication_failed":
        return {
            "alert": "FAILED_AUTHENTICATION",
            "severity": "MEDIUM",
            "message": "A user authentication attempt failed.",
            "timestamp": event.get("timestamp"),
            "username": event.get("username"),
            "source_ip": event.get("source_ip")
        }

    return None


for line in sys.stdin:
    alert = detect_event(line.strip())

    if alert:
        print(json.dumps(alert))
