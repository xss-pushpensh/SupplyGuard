#!/usr/bin/env python3
import subprocess, sys

def check(image):
    print(f"[DETECT] Verifying provenance for {image}")
    r = subprocess.run(
        f"cosign verify {image}",
        shell=True, capture_output=True, text=True
    )
    if r.returncode == 0:
        print("[OK] signature valid")
        return True
    print(f"[FAIL] no valid signature: {r.stderr.strip()[:200]}")
    return False

if __name__ == "__main__":
    img = sys.argv[1] if len(sys.argv) > 1 else "ghcr.io/example/demo:latest"
    ok = check(img)
    sys.exit(0 if ok else 1)
