#!/usr/bin/env bash
set -euo pipefail

# Usage:
# bash scripts/run-example.sh <tool> <target_url_or_domain> [options]
# Tools: gobuster, wpscan, sqlmap, nikto, wfuzz
# Options (per tool):
#   gobuster: --wordlist <path>  --mode dir|dns  --outfile <path>
#   wpscan:   --api-token <token> --outfile <path>
#   sqlmap:   --flags "--batch --risk=1" --outfile <path>
#   nikto:    --outfile <path>
#   wfuzz:    --wordlist <path> --outfile <path>

ROOT="$HOME/Desktop/fsociety_tools"
OUTDIR="$ROOT/output"
mkdir -p "$OUTDIR"

if [ -f "$ROOT/env.sh" ]; then
  # shellcheck disable=SC1090
  source "$ROOT/env.sh"
fi

TOOL="${1:-}"
TARGET="${2:-}"
shift 2 || true

# Defaults
WORDLIST_DEFAULT="$ROOT/SecLists/Discovery/Web-Content/common.txt"
MODE="dir"
OUTFILE=""
API_TOKEN=""
SQLMAP_FLAGS="--batch"
TARGET_FILE=""

# Parse options
while [ $# -gt 0 ]; do
  case "$1" in
    --wordlist)
      WORDLIST_DEFAULT="$2"; shift 2 ;;
    --mode)
      MODE="$2"; shift 2 ;;
    --outfile)
      OUTFILE="$2"; shift 2 ;;
    --api-token)
      API_TOKEN="$2"; shift 2 ;;
    --flags)
      SQLMAP_FLAGS="$2"; shift 2 ;;
    --target-file)
      TARGET_FILE="$2"; shift 2 ;;
    *)
      echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$TOOL" ] || [ -z "$TARGET" ]; then
  echo "Usage: bash scripts/run-example.sh <tool> <target_url_or_domain>"
  echo "Tools: gobuster, wpscan, sqlmap"
  exit 1
fi

timestamp() { date +"%Y%m%d-%H%M%S"; }

run_gobuster() {
  local target="$1"
  local wordlist="$2"
  local mode="$3"
  [ -n "$OUTFILE" ] || OUTFILE="$OUTDIR/gobuster-$(timestamp).txt"
  if [ "$mode" = "dns" ]; then
    echo "[run] gobuster dns -d $target -w $wordlist"
    gobuster dns -d "$target" -w "$wordlist" -o "$OUTFILE" || true
  else
    echo "[run] gobuster dir -u $target -w $wordlist"
    gobuster dir -u "$target" -w "$wordlist" -o "$OUTFILE" || true
  fi
  echo "Output: $OUTFILE"
}

run_wpscan() {
  local target="$1"
  [ -n "$OUTFILE" ] || OUTFILE="$OUTDIR/wpscan-$(timestamp).txt"
  CMD=(wpscan --url "$target")
  [ -n "$API_TOKEN" ] && CMD+=(--api-token "$API_TOKEN")
  echo "[run] ${CMD[*]}"
  "${CMD[@]}" | tee "$OUTFILE" || true
  echo "Output: $OUTFILE"
}

run_sqlmap() {
  local target="$1"
  [ -n "$OUTFILE" ] || OUTFILE="$OUTDIR/sqlmap-$(timestamp).txt"
  echo "[run] sqlmap -u $target $SQLMAP_FLAGS"
  python3 "$ROOT/sqlmap/sqlmap.py" -u "$target" $SQLMAP_FLAGS | tee "$OUTFILE" || true
  echo "Output: $OUTFILE"
}

run_nikto() {
  local target="$1"
  [ -n "$OUTFILE" ] || OUTFILE="$OUTDIR/nikto-$(timestamp).txt"
  local nikto_bin="$ROOT/nikto/program/nikto.pl"
  if [ ! -f "$nikto_bin" ]; then
    echo "Nikto not found at $nikto_bin"
    return 1
  fi
  echo "[run] nikto -h $target"
  perl "$nikto_bin" -h "$target" | tee "$OUTFILE" || true
  echo "Output: $OUTFILE"
}

run_wfuzz() {
  local target="$1"
  local wordlist="$2"
  [ -n "$OUTFILE" ] || OUTFILE="$OUTDIR/wfuzz-$(timestamp).txt"
  if [ ! -f "$wordlist" ]; then
    echo "Wordlist not found at $wordlist"
    return 1
  fi
  echo "[run] wfuzz -c -z file,$wordlist -u $target"
  wfuzz -c -z file,"$wordlist" -u "$target" | tee "$OUTFILE" || true
  echo "Output: $OUTFILE"
}

case "$TOOL" in
  gobuster)
    WORDLIST="$WORDLIST_DEFAULT"
    if [ ! -f "$WORDLIST" ]; then
      echo "Wordlist not found at $WORDLIST. Run seclists-sparse.sh first."
      exit 1
    fi
    if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
      while read -r t; do [ -n "$t" ] && run_gobuster "$t" "$WORDLIST" "$MODE"; done < "$TARGET_FILE"
    else
      run_gobuster "$TARGET" "$WORDLIST" "$MODE"
    fi
    ;;
  wpscan)
    if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
      while read -r t; do [ -n "$t" ] && run_wpscan "$t"; done < "$TARGET_FILE"
    else
      run_wpscan "$TARGET"
    fi
    ;;
  sqlmap)
    if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
      while read -r t; do [ -n "$t" ] && run_sqlmap "$t"; done < "$TARGET_FILE"
    else
      run_sqlmap "$TARGET"
    fi
    ;;
  nikto)
    if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
      while read -r t; do [ -n "$t" ] && run_nikto "$t"; done < "$TARGET_FILE"
    else
      run_nikto "$TARGET"
    fi
    ;;
  wfuzz)
    WORDLIST="$WORDLIST_DEFAULT"
    if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
      while read -r t; do [ -n "$t" ] && run_wfuzz "$t" "$WORDLIST"; done < "$TARGET_FILE"
    else
      run_wfuzz "$TARGET" "$WORDLIST"
    fi
    ;;
  *)
    echo "Unknown tool: $TOOL"
    echo "Tools: gobuster, wpscan, sqlmap, nikto, wfuzz"
    exit 1
    ;;
esac

echo "Done."
