import json
import sys
from collections import defaultdict

failed_auth_attempts = defaultdict(int)

BRUTE_FORCE_THRESHOLD = 5


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
        source_ip = event.get("source_ip", "unknown")

        failed_auth_attempts[source_ip] += 1

        if failed_auth_attempts[source_ip] >= BRUTE_FORCE_THRESHOLD:
            return {
                "alert": "BRUTE_FORCE_DETECTED",
                "severity": "HIGH",
                "message": "Multiple failed authentication attempts detected.",
                "timestamp": event.get("timestamp"),
                "source_ip": source_ip,
                "attempts": failed_auth_attempts[source_ip]
            }

        return {
            "alert": "FAILED_AUTHENTICATION",
            "severity": "MEDIUM",
            "message": "A user authentication attempt failed.",
            "timestamp": event.get("timestamp"),
            "username": event.get("username"),
            "source_ip": source_ip
        }

    return None


for line in sys.stdin:
    alert = detect_event(line.strip())

    if alert:
        print(json.dumps(alert))
