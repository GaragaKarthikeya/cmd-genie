#!/bin/bash

# Installation script for cmd-genie - Wish Terminal Helper
echo "Installing cmd-genie - Your magical command assistant..."

# Get the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

# Install man page
echo "Installing man page..."
if [ -w "/usr/local/share/man/man1" ] || sudo -n true 2>/dev/null; then
    sudo mkdir -p /usr/local/share/man/man1
    sudo cp "$SCRIPT_DIR/cmd-genie.1" /usr/local/share/man/man1/
    # Create symlink so both 'man cmd-genie' and 'man wish' work
    sudo ln -sf /usr/local/share/man/man1/cmd-genie.1 /usr/local/share/man/man1/wish.1
    sudo mandb -q 2>/dev/null || true
    echo "✓ Man page installed (try 'man cmd-genie' or 'man wish')"
else
    # Fallback to user man directory
    mkdir -p ~/.local/share/man/man1
    cp "$SCRIPT_DIR/cmd-genie.1" ~/.local/share/man/man1/
    ln -sf ~/.local/share/man/man1/cmd-genie.1 ~/.local/share/man/man1/wish.1
    echo "✓ Man page installed to user directory"
    echo "  Note: Add ~/.local/share/man to MANPATH if needed"
fi

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