#!/bin/bash
# Quick network scan with AI analysis
# Usage: ./quick_scan.sh <target>

TARGET=${1:-"192.168.1.0/24"}
RESULTS_DIR="$(dirname "$0")/../results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="$RESULTS_DIR/scan_${TIMESTAMP}.txt"

echo "🔍 Scanning: $TARGET"
echo "📁 Output: $OUTPUT_FILE"
echo ""

# Run nmap scan
nmap -sV -sC -oN "$OUTPUT_FILE" "$TARGET"

echo ""
echo "✅ Scan complete!"
echo ""
echo "🤖 Sending to LLM for analysis..."

# Send to Ollama for analysis
SCAN_RESULTS=$(cat "$OUTPUT_FILE")

curl -s http://localhost:11434/api/generate -d "{
  \"model\": \"dolphin-mistral\",
  \"prompt\": \"Analyze this nmap scan and identify: 1) Open ports and services 2) Potential vulnerabilities 3) Recommended next steps. Be concise.\n\nScan results:\n$SCAN_RESULTS\",
  \"stream\": false
}" | jq -r '.response' | tee "$RESULTS_DIR/analysis_${TIMESTAMP}.txt"

echo ""
echo "📄 Analysis saved to: $RESULTS_DIR/analysis_${TIMESTAMP}.txt"
