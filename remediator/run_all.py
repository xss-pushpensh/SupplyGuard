#!/usr/bin/env python3
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMO = ROOT / "demo-pipeline"

def pin_actions(path):
    """SHA-pin GitHub Actions."""
    text = path.read_text()
    fixes = {
        "actions/checkout@v3":  "actions/checkout@8e5e7e5ab8b370d6c329ec480221332ada57f0ab",
        "actions/setup-node@v3": "actions/setup-node@64ed1c7eab4cce3362f8c340dee64e5eaeef8f28",
    }
    changed = False
    for old, new in fixes.items():
        if old in text:
            text = text.replace(old, new)
            changed = True
    if changed:
        path.write_text(text)
        print(f"[FIX] SHA-pinned actions in {path.name}")

def pin_dependencies(path):
    """Add SHA pin comment placeholder for suspicious deps."""
    data = json.loads(path.read_text())
    deps = data.get("dependencies", {})
    for name in list(deps.keys()):
        if name in ("lodahs",):  # typosquat target
            print(f"[FIX] Removing suspicious dependency: {name}")
            del deps[name]
            data["dependencies"] = deps
            path.write_text(json.dumps(data, indent=2))
            return True
    return False

def add_cosign_step(workflow):
    text = workflow.read_text()
    if "cosign verify" in text:
        return False
    inject = """      - name: Verify provenance
        run: cosign verify ${{ env.IMAGE }} || exit 1
"""
    text = text.replace("      - run: node index.js",
                        "      - run: node index.js\n" + inject)
    workflow.write_text(text)
    print("[FIX] Added cosign verification step")
    return True

def main():
    fixes = []
    wf = DEMO / ".github/workflows/build.yml"
    pkg = DEMO / "package.json"

    if wf.exists() and pin_actions(wf):
        fixes.append("pinned_github_actions")
    if wf.exists() and add_cosign_step(wf):
        fixes.append("added_cosign_verification")
    if pkg.exists() and pin_dependencies(pkg):
        fixes.append("removed_typosquat_dependency")

    report = ROOT / "reports" / "remediation.json"
    report.write_text(json.dumps({"fixes": fixes}, indent=2))
    print(f"\n[FIX] Remediation report -> {report}")
    print(json.dumps({"fixes": fixes}, indent=2))

if __name__ == "__main__":
    main()
