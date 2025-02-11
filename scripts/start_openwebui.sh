#!/bin/bash

# Ensure Python and Pip are installed
if ! command -v python3 &>/dev/null; then
    echo "Python3 is not installed. Installing..."
    pkg install python -y
fi

if ! command -v pip &>/dev/null; then
    echo "Pip is not installed. Installing..."
    pkg install python-pip -y
fi

# Install Open WebUI if not already installed
if ! pip show open-webui &>/dev/null; then
    echo "Installing Open WebUI..."
    pip install open-webui
fi

# Ensure Open WebUI is in the path
export PATH=$HOME/.local/bin:$PATH

# Run Open WebUI
echo "Starting Open WebUI..."
open-webui serve
