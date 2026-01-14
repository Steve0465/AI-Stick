#!/usr/bin/env bash
set -euo pipefail

# Batch runner: executes multiple tool invocations from a simple JSON file.
# Usage:
#   bash scripts/run-batch.sh /path/to/plan.json
# Plan format example:
# {
#   "env": true,
#   "jobs": [
#     {"tool": "gobuster", "target": "https://example.com", "options": {"mode": "dir", "wordlist": "~/Desktop/fsociety_tools/SecLists/Discovery/Web-Content/common.txt"}},
#     {"tool": "wpscan",   "target": "https://example.com", "options": {"api_token": "YOUR_TOKEN"}},
#     {"tool": "sqlmap",   "target": "https://example.com/item.php?id=1", "options": {"flags": "--batch --risk=1"}}
#     {"tool": "nikto",    "target": "https://example.com"}
#     {"tool": "wfuzz",    "target": "https://example.com/page?user=FUZZ", "options": {"wordlist": "~/Desktop/fsociety_tools/SecLists/Discovery/Web-Content/common.txt"}}
#   ]
# }

ROOT="$HOME/Desktop/fsociety_tools"
OUTDIR="$ROOT/output"
mkdir -p "$OUTDIR"

PLAN_FILE="${1:-}"
if [ -z "$PLAN_FILE" ] || [ ! -f "$PLAN_FILE" ]; then
  echo "Provide a JSON plan file. See usage header for example."
  exit 1
fi

if command -v jq >/dev/null 2>&1; then
  :
else
  echo "jq is required. Install: brew install jq"
  exit 1
fi

# Optionally source environment
USE_ENV=$(jq -r '.env // false' "$PLAN_FILE")
if [ "$USE_ENV" = "true" ] && [ -f "$ROOT/env.sh" ]; then
  # shellcheck disable=SC1090
  source "$ROOT/env.sh"
fi

ts() { date +"%Y%m%d-%H%M%S"; }

JOBS_LEN=$(jq '.jobs | length' "$PLAN_FILE")
echo "[batch] Running $JOBS_LEN jobs from $PLAN_FILE"

for i in $(jq -r '.jobs | keys[]' "$PLAN_FILE"); do
  TOOL=$(jq -r ".jobs[$i].tool" "$PLAN_FILE")
  TARGET=$(jq -r ".jobs[$i].target" "$PLAN_FILE")
  OUTFILE="$OUTDIR/${TOOL}-$(ts).txt"
  echo "[job:$i] $TOOL -> $TARGET"

  case "$TOOL" in
    gobuster)
      MODE=$(jq -r ".jobs[$i].options.mode // \"dir\"" "$PLAN_FILE")
      WORDLIST=$(jq -r ".jobs[$i].options.wordlist // \"$ROOT/SecLists/Discovery/Web-Content/common.txt\"" "$PLAN_FILE")
      [ -f "$WORDLIST" ] || { echo "Missing wordlist: $WORDLIST"; continue; }
      if [ "$MODE" = "dns" ]; then
        echo "[run] gobuster dns -d $TARGET -w $WORDLIST"
        gobuster dns -d "$TARGET" -w "$WORDLIST" -o "$OUTFILE" || true
      else
        echo "[run] gobuster dir -u $TARGET -w $WORDLIST"
        gobuster dir -u "$TARGET" -w "$WORDLIST" -o "$OUTFILE" || true
      fi
      echo "[out] $OUTFILE"
      ;;
    wpscan)
      API_TOKEN=$(jq -r ".jobs[$i].options.api_token // \"\"" "$PLAN_FILE")
      if [ -n "$API_TOKEN" ]; then
        wpscan --url "$TARGET" --api-token "$API_TOKEN" | tee "$OUTFILE" || true
      else
        wpscan --url "$TARGET" | tee "$OUTFILE" || true
      fi
      echo "[out] $OUTFILE"
      ;;
    sqlmap)
          nikto)
            NIKTO_BIN="$ROOT/nikto/program/nikto.pl"
            [ -f "$NIKTO_BIN" ] || { echo "Nikto not found at $NIKTO_BIN"; continue; }
            echo "[run] nikto -h $TARGET"
            perl "$NIKTO_BIN" -h "$TARGET" | tee "$OUTFILE" || true
            echo "[out] $OUTFILE"
            ;;
          wfuzz)
            WORDLIST=$(jq -r ".jobs[$i].options.wordlist // \"$ROOT/SecLists/Discovery/Web-Content/common.txt\"" "$PLAN_FILE")
            [ -f "$WORDLIST" ] || { echo "Missing wordlist: $WORDLIST"; continue; }
            echo "[run] wfuzz -c -z file,$WORDLIST -u $TARGET"
            wfuzz -c -z file,"$WORDLIST" -u "$TARGET" | tee "$OUTFILE" || true
            echo "[out] $OUTFILE"
            ;;
      FLAGS=$(jq -r ".jobs[$i].options.flags // \"--batch\"" "$PLAN_FILE")
      echo "[run] sqlmap -u $TARGET $FLAGS"
      python3 "$ROOT/sqlmap/sqlmap.py" -u "$TARGET" $FLAGS | tee "$OUTFILE" || true
      echo "[out] $OUTFILE"
      ;;
    *)
      echo "Unknown tool: $TOOL (job $i)" ;;
  esac
done

echo "[batch] Completed. Outputs in $OUTDIR"
