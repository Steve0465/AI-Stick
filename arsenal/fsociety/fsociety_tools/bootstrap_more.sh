#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/Desktop/fsociety_tools"
mkdir -p "$ROOT"
cd "$ROOT"

more_repos=(
  "https://github.com/sullo/nikto"
  "https://github.com/xmendez/wfuzz"
  "https://github.com/OJ/gobuster"
  "https://github.com/andresriancho/w3af"
  "https://github.com/vanhauser-thc/thc-hydra"
)

for r in "${more_repos[@]}"; do
  name=$(basename "$r")
  if [ -d "$ROOT/$name/.git" ]; then
    echo "SKIP: $name already cloned"
  else
    echo "Cloning $name..."
    git clone --depth=1 "$r" "$name" || echo "WARN: Failed to clone $name"
  fi
done

echo "Bootstrap of additional tools complete."
