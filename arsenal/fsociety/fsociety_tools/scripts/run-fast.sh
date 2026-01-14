s#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$HOME/Desktop/fsociety_tools"
SMALL_DIR="$ROOT_DIR/wordlists-small"
SEC_DIR="$ROOT_DIR/SecLists"
RUN_EX="$ROOT_DIR/scripts/run-example.sh"

usage() {
  echo "Usage: run-fast.sh <tool> <target> [--mode dir|dns] [--flags '...']"
  echo "Defaults: web paths -> web-common.txt, DNS -> dns-small.txt"
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" || $# -lt 2 ]]; then
  usage
  exit 0
fi

TOOL="$1"; shift
TARGET="$1"; shift
MODE="dir"
FLAGS=""
WORDLIST=""

while (( "$#" )); do
  case "$1" in
    --mode)
      MODE="$2"; shift 2 ;;
    --flags)
      FLAGS="$2"; shift 2 ;;
    --wordlist)
      WORDLIST="$2"; shift 2 ;;
    *)
      # pass-through unknowns
      shift ;;
  esac
done

# Choose defaults only if user didn't provide --wordlist
if [[ -z "$WORDLIST" ]]; then
  case "$TOOL:$MODE" in
    gobuster:dir)
      WORDLIST="$SMALL_DIR/web-common.txt" ;;
    gobuster:dns)
      WORDLIST="$SMALL_DIR/dns-small.txt" ;;
    wfuzz:dir|wfuzz:*)
      WORDLIST="$SMALL_DIR/web-common.txt" ;;
    *)
      WORDLIST=""
      ;;
  esac
fi

# Build passthrough args to run-example
ARGS=("$TOOL" "$TARGET")
if [[ -n "$WORDLIST" ]]; then
  ARGS+=("--wordlist" "$WORDLIST")
fi
if [[ -n "$FLAGS" ]]; then
  ARGS+=("--flags" "$FLAGS")
fi
if [[ -n "$MODE" ]]; then
  ARGS+=("--mode" "$MODE")
fi

bash "$RUN_EX" "${ARGS[@]}"
