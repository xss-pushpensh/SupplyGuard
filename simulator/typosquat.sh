#!/bin/sh
set -e
mkdir -p /tmp/typo && cd /tmp/typo
cat > package.json <<'PKG'
{
  "name": "lodahs",
  "version": "4.17.20",
  "description": "typosquat of lodash"
}
PKG
cat > index.js <<'JS'
console.log("[ATTACK] typosquat payload executed");
JS
npm config set registry http://verdaccio:4873
npm publish --registry http://verdaccio:4873 || true
echo "[SIM] Typosquatting package published"
