#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/Desktop/fsociety_tools"
SECLISTS_DIR="$ROOT/SecLists"

echo "[seclists-sparse] Preparing sparse checkout..."
rm -rf "$SECLISTS_DIR"
git clone --filter=blob:none --no-checkout https://github.com/danielmiessler/SecLists "$SECLISTS_DIR"
cd "$SECLISTS_DIR"
git sparse-checkout init --cone
git sparse-checkout set Discovery/Web-Content Discovery/DNS Passwords/Leaked-Databases
git checkout

echo "[seclists-sparse] Complete. Subsets fetched:"
du -sh "$SECLISTS_DIR"/* 2>/dev/null | sort -h | tail -n 10 || true
