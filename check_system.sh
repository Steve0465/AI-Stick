#!/bin/bash
# System Check - Verify AI_STICK is ready to use

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           AI_STICK SYSTEM CHECK                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo

# Check if running on Pi
echo "🔍 Checking system..."
if [ -f /proc/device-tree/model ]; then
    MODEL=$(cat /proc/device-tree/model)
    echo "   ✅ Running on: $MODEL"
else
    echo "   ⚠️  Not running on Raspberry Pi"
fi
echo

# Check Ollama
echo "🤖 Checking Ollama..."
if systemctl is-active --quiet ollama; then
    echo "   ✅ Ollama is running"
    
    # Check models
    if command -v ollama &> /dev/null; then
        echo "   📦 Installed models:"
        ollama list | tail -n +2 | awk '{print "      -", $1, "(" $2 ")"}'
    fi
else
    echo "   ❌ Ollama is not running"
    echo "      Start with: sudo systemctl start ollama"
fi
echo

# Check Python packages
echo "🐍 Checking Python..."
if python3 -c "import requests" 2>/dev/null; then
    echo "   ✅ python3-requests installed"
else
    echo "   ❌ python3-requests missing"
    echo "      Install with: sudo apt install python3-requests"
fi

if python3 -c "import tqdm" 2>/dev/null; then
    echo "   ✅ python3-tqdm installed"
else
    echo "   ⚠️  python3-tqdm missing (optional)"
fi
echo

# Check Tailscale
echo "🔐 Checking Tailscale..."
if command -v tailscale &> /dev/null; then
    if tailscale status &> /dev/null; then
        echo "   ✅ Tailscale connected"
        IP=$(tailscale ip -4 2>/dev/null)
        if [ -n "$IP" ]; then
            echo "      IP: $IP"
        fi
    else
        echo "   ⚠️  Tailscale installed but not connected"
        echo "      Connect with: sudo tailscale up"
    fi
else
    echo "   ❌ Tailscale not installed"
fi
echo

# Check AI tools
echo "🛠️  Checking AI tools..."
TOOLS=(
    "quick_ai.py:Quick AI chat"
    "code_writer.py:Code generator"
    "coding_agent.py:Interactive coding agent"
    "ai_agent.py:File analyzer"
    "smart_ai.py:Knowledge-based AI"
    "index_knowledge.py:Knowledge indexer"
)

for tool_info in "${TOOLS[@]}"; do
    IFS=':' read -r tool desc <<< "$tool_info"
    if [ -f "$tool" ] && [ -x "$tool" ]; then
        echo "   ✅ $desc ($tool)"
    else
        echo "   ❌ $desc ($tool) - missing or not executable"
    fi
done
echo

# Check knowledge base index
echo "📚 Checking knowledge base..."
if [ -f "/tmp/ai_stick_index.json" ]; then
    echo "   ✅ Knowledge base indexed"
elif [ -f ".ai_index.json" ]; then
    echo "   ✅ Knowledge base indexed"
else
    echo "   ⚠️  Knowledge base not indexed"
    echo "      Index with: ./index_knowledge.py"
fi
echo

# Summary
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                    QUICK START                            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo
echo "🚀 Interactive coding with Mistral:"
echo "   ./coding_agent.py"
echo
echo "💬 Quick questions:"
echo "   ./quick_ai.py 'your question'"
echo
echo "📝 Generate code:"
echo "   ./code_writer.py 'what you want to build'"
echo
echo "🧠 Knowledge-based queries:"
echo "   ./smart_ai.py 'what tools do I have?'"
echo
echo "📖 Full documentation:"
echo "   cat AI_TOOLS_README.md"
echo
