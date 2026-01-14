#!/bin/bash
cd "$(dirname "$0")"

# Path to portable python (if installed)
PORTABLE_PYTHON="./_portable_runtimes/mac_python/bin/python3"
SCRIPT="./janitor.py"

echo "Checking for Portable Python..."
if [ -f "$PORTABLE_PYTHON" ]; then
    echo "Found Portable Python. Launching..."
    "$PORTABLE_PYTHON" "$SCRIPT"
else
    echo "[WARNING] Portable Python not found at $PORTABLE_PYTHON"
    echo "Attempting to use system Python3..."
    if command -v python3 &> /dev/null; then
        python3 "$SCRIPT"
    else
        echo "[ERROR] Python3 is not installed on this system."
        echo "Please install Python or set up the portable runtime."
        read -p "Press Enter to exit..."
    fi
fi
