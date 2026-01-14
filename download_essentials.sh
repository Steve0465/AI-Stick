#!/bin/bash
#
# AI_STICK Essential Downloads
# Run this to grab the priority items
#

STICK="/Volumes/AI_STICK"
cd "$STICK"

echo "========================================"
echo "🚀 AI_STICK ESSENTIAL DOWNLOADS"
echo "========================================"
echo ""

# Create folders
mkdir -p models/whisper
mkdir -p models/gguf
mkdir -p _portable_tools/kiwix

echo "📥 Downloading Whisper models..."
cd models/whisper

# Whisper - base is good enough for most, small for accuracy
if [ ! -f "ggml-base.en.bin" ]; then
    curl -L -o ggml-base.en.bin "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
fi

if [ ! -f "ggml-small.en.bin" ]; then
    curl -L -o ggml-small.en.bin "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-small.en.bin"
fi

echo "✅ Whisper models done"
echo ""

echo "📥 Getting Kiwix (for reading your ZIM files)..."
cd "$STICK/_portable_tools"
if [ ! -d "kiwix" ] || [ -z "$(ls -A kiwix 2>/dev/null)" ]; then
    # macOS version
    curl -L -o kiwix.dmg "https://download.kiwix.org/release/kiwix-desktop/kiwix-desktop_macos.dmg"
    echo "   Downloaded kiwix.dmg - mount it and copy Kiwix.app to the kiwix folder"
fi

echo ""
echo "========================================"
echo "🧠 OLLAMA MODELS (run separately)"
echo "========================================"
echo ""
echo "Run these commands to download models:"
echo ""
echo "  # Small models (Pi-friendly)"
echo "  ollama pull phi3:mini"
echo "  ollama pull tinyllama"
echo "  ollama pull qwen2.5:3b"
echo ""
echo "  # Vision model (can read images!)"
echo "  ollama pull llava:7b"
echo ""
echo "  # Coding model"
echo "  ollama pull codellama:7b"
echo ""
echo "========================================"
echo "📚 ZIM FILES TO DOWNLOAD"
echo "========================================"
echo ""
echo "Go to: https://library.kiwix.org"
echo ""
echo "Priority downloads:"
echo "  1. khan_academy_en_all.zim (~40GB)"
echo "  2. wikihow_en_all.zim (~15GB)"
echo "  3. ifixit_en_all.zim (~3GB)"
echo ""
echo "========================================"
echo "✅ DONE! Check models/whisper for Whisper"
echo "========================================"

ls -lh "$STICK/models/whisper/"
