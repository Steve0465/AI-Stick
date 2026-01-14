#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/Desktop/fsociety_tools"

echo "[smoke] Setting environment..."
if [ -f "$ROOT/env.sh" ]; then
  # shellcheck disable=SC1090
  source "$ROOT/env.sh"
fi

echo "[smoke] Tool versions/help"
echo "- nmap:"
nmap -V || echo "nmap not available"

echo "- sqlmap:"
python3 "$ROOT/sqlmap/sqlmap.py" -hh | head -n 10 || echo "sqlmap not available"

echo "- XSStrike:"
python3 "$ROOT/XSStrike/xsstrike.py" -h | head -n 10 || echo "XSStrike not available"

echo "- commix:"
python3 "$ROOT/commix/commix.py" --help | head -n 10 || echo "commix not available"

echo "- wpscan:"
wpscan --help | head -n 10 || echo "wpscan not on PATH; try 'source $ROOT/env.sh'"

echo "- pixiewps:"
"$ROOT/pixiewps/pixiewps" -h | head -n 10 || echo "pixiewps binary not built"

echo "- gobuster:"
gobuster -h | head -n 10 || echo "gobuster not available"

echo "[smoke] Done."
