#!/bin/bash

# Installation script for cmd-genie - Wish Terminal Helper
echo "Installing cmd-genie - Your magical command assistant..."

# Get the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

# Add to bashrc if not already there
if ! grep -q "# cmd-genie - Wish Terminal Helper" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# cmd-genie - Wish Terminal Helper" >> ~/.bashrc
    echo "source $SCRIPT_DIR/x_function.sh" >> ~/.bashrc
    echo "✓ Added wish function to ~/.bashrc"
else
    echo "✓ wish function already in ~/.bashrc"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Setup your Gemini API key:"
echo "  export GEMINI_API_KEY='your-api-key-here'"
echo "  # Add this to your ~/.bashrc to make it permanent"
echo ""
echo "Usage:"
echo "  wish 'list all files'     # Your wish appears ready to redeem"
echo "  wish 'copy a file'        # Press ↑ then Enter to execute"
echo "  wish 'show processes'     # Simple and magical"
echo ""
echo "Restart your terminal or run: source ~/.bashrc"