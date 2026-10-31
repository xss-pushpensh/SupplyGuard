#!/usr/bin/env python3
import subprocess, json, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
SBOM_DIR = ROOT / "sboms"
SBOM_DIR.mkdir(exist_ok=True)

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout, r.stderr, r.returncode

def sbom(target, tag):
    out = SBOM_DIR / f"{tag}.json"
    print(f"[DETECT] Generating SBOM for {target} -> {out.name}")
    _, err, rc = run(f"syft {target} -o json > {out}")
    if rc != 0:
        print(f"[!] syft error: {err}")
        return None
    return out

def diff_sboms(a, b):
    def load(p):
        data = json.loads(Path(p).read_text())
        return {(pkg["name"], pkg.get("version","?")) for pkg in data.get("artifacts", [])}
    A, B = load(a), load(b)
    added   = B - A
    removed = A - B
    return {"added": list(added), "removed": list(removed)}

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "demo-pipeline")
    before = sbom(target, "before")
    # simulate change: modify package.json then scan again
    pkg = Path(target) / "package.json"
    original = pkg.read_text()
    tampered = original.replace('"lodash": "4.17.20"',
                                '"lodash": "4.17.20",\n    "lodahs": "4.17.20"')
    pkg.write_text(tampered)
    after = sbom(target, "after")
    pkg.write_text(original)

    diff = diff_sboms(before, after)
    out = ROOT / "reports" / "sbom_diff.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(diff, indent=2))
    print(f"[DETECT] SBOM diff: {diff}")
    print(f"[DETECT] Written to {out}")

if __name__ == "__main__":
    main()
