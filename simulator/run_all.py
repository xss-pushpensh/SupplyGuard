#!/usr/bin/env python3
import subprocess, sys, json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT.parent / "reports"
REPORT.mkdir(exist_ok=True)

def run(cmd, cwd=None):
    print(f"[SIM] $ {cmd}")
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if r.stdout: print(r.stdout.strip())
    if r.stderr: print(r.stderr.strip())
    return r.returncode

def attack_dep_confusion():
    print("\n=== Attack 1: Dependency Confusion ===")
    run("docker exec sg-attacker sh /attack/dep_confusion.sh")

def attack_typosquat():
    print("\n=== Attack 2: Typosquatting ===")
    run("docker exec sg-attacker sh /attack/typosquat.sh")

def attack_action():
    print("\n=== Attack 3: Malicious GitHub Action ===")
    print("[SIM] malicious-action/action.yml staged (would be used in workflow)")

def attack_tamper():
    print("\n=== Attack 4: Artifact Tampering ===")
    tmp = "/tmp/build-artifact.tar.gz"
    run(f"echo 'legit-build' > {tmp}")
    run(f"sh {ROOT}/tamper_artifact.sh {tmp}")

def main():
    attacks = {
        "dep_confusion": attack_dep_confusion,
        "typosquat":     attack_typosquat,
        "malicious_action": attack_action,
        "artifact_tamper":  attack_tamper,
    }
    results = {}
    for name, fn in attacks.items():
        try:
            fn()
            results[name] = "simulated"
        except Exception as e:
            results[name] = f"error: {e}"
    (REPORT / "simulation.json").write_text(json.dumps(results, indent=2))
    print("\n[SIM] Report written to reports/simulation.json")

if __name__ == "__main__":
    main()
