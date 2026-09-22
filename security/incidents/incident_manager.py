import json
import sys
from datetime import datetime
from pathlib import Path


INCIDENT_FILE = Path(__file__).parent / "incidents.jsonl"


def create_incident(alert):
    return {
        "incident_id": f"INC-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
        "alert": alert.get("alert"),
        "severity": alert.get("severity"),
        "status": "OPEN",
        "timestamp": alert.get("timestamp"),
        "source_ip": alert.get("source_ip"),
        "description": alert.get("message"),
        "response": {
            "action": "PENDING",
            "timestamp": None
        }
    }


for line in sys.stdin:
    try:
        alert = json.loads(line)
    except json.JSONDecodeError:
        continue

    incident = create_incident(alert)

    with INCIDENT_FILE.open("a") as file:
        file.write(json.dumps(incident) + "\n")

    print(json.dumps(incident, indent=2))
