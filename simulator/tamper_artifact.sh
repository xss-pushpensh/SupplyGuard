#!/bin/sh
# Simulates post-build artifact tampering
set -e
ARTIFACT="${1:-/tmp/build-artifact.tar.gz}"
echo "[SIM] original artifact: $ARTIFACT"
echo "malicious-payload" >> "$ARTIFACT"
echo "[SIM] artifact tampered (hash changed)"
sha256sum "$ARTIFACT"
