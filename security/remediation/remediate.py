import json
import sys
from datetime import datetime
from pathlib import Path


REMEDIATION_FILE = Path(__file__).parent / "remediation.jsonl"


def remediate(incident):
    timestamp = datetime.utcnow().isoformat() + "Z"

    if incident.get("alert") == "BRUTE_FORCE_DETECTED":
        source_ip = incident.get("source_ip")

        return {
            "incident_id": incident.get("incident_id"),
            "action": "BLOCK_SOURCE_IP",
            "source_ip": source_ip,
            "status": "SIMULATED",
            "timestamp": timestamp,
            "message": f"Simulated blocking of source IP {source_ip}."
        }

    return {
        "incident_id": incident.get("incident_id"),
        "action": "NO_ACTION",
        "status": "NOT_REQUIRED",
        "timestamp": timestamp
    }


for line in sys.stdin:
    try:
        incident = json.loads(line)
    except json.JSONDecodeError:
        continue

    result = remediate(incident)

    with REMEDIATION_FILE.open("a") as file:
        file.write(json.dumps(result) + "\n")

    print(json.dumps(result, indent=2))
