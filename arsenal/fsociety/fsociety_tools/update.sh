#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/Desktop/fsociety_tools"
VENVDIR="$ROOT/.venv"

echo "[fsociety_tools] Updating cloned tool repositories..."
cd "$ROOT"

repos=(
  nmap
  sqlmap
  wpscan
  XSStrike
  commix
  reaver-wps-fork-t6x
  pixiewps
  social-engineer-toolkit
  ncrack
  cupp
)

for r in "${repos[@]}"; do
  if [ -d "$ROOT/$r/.git" ]; then
    echo "→ $r"
    (cd "$ROOT/$r" && git pull --ff-only || echo "WARN: git pull failed for $r")
  else
    echo "SKIP: $r not a git repo"
  fi
done

echo "\n[fsociety_tools] Updating Homebrew packages..."
if command -v brew >/dev/null 2>&1; then
  brew update || true
  brew upgrade python nmap ncrack ruby openssl libffi || true
else
  echo "Homebrew not found; skipping brew upgrade."
fi

echo "\n[fsociety_tools] Updating Ruby gems for wpscan..."
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
if command -v gem >/dev/null 2>&1; then
  gem install bundler -v 2.4.22 || true
  gem install public_suffix -v 5.1.1 || true
  gem install wpscan || true
  # Ensure wpscan is on PATH after gem install
  hash wpscan 2>/dev/null && wpscan --update || echo "wpscan not on PATH; try 'source env.sh' then rerun."
else
  echo "Ruby gem not available; skipping wpscan gem updates."
fi

echo "\n[fsociety_tools] Updating Python venv dependencies (SET)..."
if [ -d "$VENVDIR" ]; then
  source "$VENVDIR/bin/activate"
  python -m pip install --upgrade pip || true
  if [ -f "$ROOT/social-engineer-toolkit/requirements.txt" ]; then
    python -m pip install -r "$ROOT/social-engineer-toolkit/requirements.txt" || true
  fi
  deactivate || true
else
  echo "Python venv not found; creating one..."
  python3 -m venv "$VENVDIR"
  source "$VENVDIR/bin/activate"
  python -m pip install --upgrade pip || true
  if [ -f "$ROOT/social-engineer-toolkit/requirements.txt" ]; then
    python -m pip install -r "$ROOT/social-engineer-toolkit/requirements.txt" || true
  fi
  deactivate || true
fi

echo "\n[fsociety_tools] Rebuilding native tools (pixiewps; reaver if possible)..."
if [ -f "$ROOT/pixiewps/Makefile" ]; then
  (cd "$ROOT/pixiewps" && make || true)
fi

if [ -f "$ROOT/reaver-wps-fork-t6x/configure" ]; then
  (cd "$ROOT/reaver-wps-fork-t6x" && ./configure || true && make || true)
else
  echo "Reaver configure script not present or macOS wireless stack unsupported; skipping."
fi

echo "\n[fsociety_tools] Update complete."
