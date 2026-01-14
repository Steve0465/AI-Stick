#!/usr/bin/env bash
# Source this to set environment for tools
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
if [ -d "$HOME/Desktop/fsociety_tools/.venv" ]; then
  source "$HOME/Desktop/fsociety_tools/.venv/bin/activate"
fi
echo "Environment set. Ruby PATH added; Python venv activated if present."
