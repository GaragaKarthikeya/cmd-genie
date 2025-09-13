#!/bin/bash

# Installation script for X - LLM Terminal Helper
echo "Installing X - LLM Terminal Helper..."

# Get the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

# Add to bashrc if not already there
if ! grep -q "# X - LLM Terminal Helper" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# X - LLM Terminal Helper" >> ~/.bashrc
    echo "source $SCRIPT_DIR/x_function.sh" >> ~/.bashrc
    echo "✓ Added X function to ~/.bashrc"
else
    echo "✓ X function already in ~/.bashrc"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Setup your Gemini API key:"
echo "  export GEMINI_API_KEY='your-api-key-here'"
echo "  # Add this to your ~/.bashrc to make it permanent"
echo ""
echo "Usage:"
echo "  x 'list all files'     # Command appears ready to execute"
echo "  x 'copy a file'        # Just press Enter to run"
echo "  x 'show processes'     # Simple and fast"
echo ""
echo "Restart your terminal or run: source ~/.bashrc"