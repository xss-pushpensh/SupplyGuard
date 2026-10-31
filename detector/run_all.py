#!/usr/bin/env python3
import json, subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "reports" / "findings.json"

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout, r.stderr, r.returncode

def detect_sbom():
    out, err, rc = run(f"python3 {ROOT}/detector/sbom_scan.py")
    print(out)
    try:
        return json.loads((ROOT / "reports" / "sbom_diff.json").read_text())
    except Exception:
        return {"added": [], "removed": []}

def detect_policy(payload_path):
    if not Path(payload_path).exists():
        return []
    out, err, rc = run(
        f"opa eval --format=json --data {ROOT}/policies/supply_chain.rego "
        f"--input {payload_path} 'data.supplyguard.deny'"
    )
    try:
        return json.loads(out)["result"][0]["expressions"][0]["value"]
    except Exception:
        return []

def main():
    findings = {
        "timestamp": datetime.utcnow().isoformat(),
        "sbom_diff": detect_sbom(),
        "policy_denials": [],
    }

    # Build a synthetic input for policy check
    payload = {
        "type": "github_action",
        "name": "actions/checkout",
        "ref": "v3"     # unpinned -> should deny
    }
    tmp = ROOT / "reports" / "_policy_input.json"
    tmp.parent.mkdir(exist_ok=True)
    tmp.write_text(json.dumps(payload))
    findings["policy_denials"] = detect_policy(tmp)

    findings["risk_score"] = (
        len(findings["sbom_diff"]["added"]) * 20 +
        len(findings["policy_denials"]) * 25
    )

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(findings, indent=2))
    print(f"\n[DETECT] Findings -> {REPORT}")
    print(json.dumps(findings, indent=2))

if __name__ == "__main__":
    main()
