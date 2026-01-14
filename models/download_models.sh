#!/bin/bash
# Run this from within Kali after installing Ollama

echo "🧠 Downloading AI Models for AI Stick..."

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Set model storage to stick
export OLLAMA_MODELS=/mnt/AI_STICK/models

# Pull models (largest to smallest)
echo "Pulling dolphin-mixtral (26GB) - Uncensored coding beast..."
ollama pull dolphin-mixtral:8x7b

echo "Pulling deepseek-coder:33b (19GB) - Code generation..."
ollama pull deepseek-coder:33b

echo "Pulling codellama:34b (19GB) - Meta's coding model..."
ollama pull codellama:34b

echo "Pulling llama3:70b-q4 (40GB) - Smartest general model..."
ollama pull llama3:70b

echo "Pulling mistral-large (40GB) - Strong reasoning..."
ollama pull mistral-large

echo "Pulling qwen2.5-coder:32b (18GB) - Alibaba's coder..."
ollama pull qwen2.5-coder:32b

echo "Pulling phi4:14b (9GB) - Microsoft's efficient model..."
ollama pull phi4:14b

echo "Pulling nomic-embed-text (274MB) - Embeddings..."
ollama pull nomic-embed-text

echo ""
echo "✅ All models downloaded!"
echo "Total: ~170GB of AI models"
