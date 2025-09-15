#!/bin/bash
#
# Installation script for cmd-genie.
# This script installs dependencies, sets up the man page, and configures
# the user's shell to use the `wish` command.
#

echo "Installing cmd-genie - Your magical command assistant..."

# Determine the absolute path of the script's directory.
# This ensures that the script can be run from any location.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Install required Python packages using pip.
echo "Installing Python dependencies..."
pip3 install -r "$SCRIPT_DIR/requirements.txt"

# Install the man page for cmd-genie.
echo "Installing man page..."
# Check if we have write permissions to the system-wide man page directory
# or if we can use sudo without a password prompt.
if [ -w "/usr/local/share/man/man1" ] || sudo -n true 2>/dev/null; then
    # Install for all users.
    sudo mkdir -p /usr/local/share/man/man1
    sudo cp "$SCRIPT_DIR/cmd-genie.1" /usr/local/share/man/man1/
    # Create a symlink so that `man wish` also works.
    sudo ln -sf /usr/local/share/man/man1/cmd-genie.1 /usr/local/share/man/man1/wish.1
    # Update the man page database.
    sudo mandb -q 2>/dev/null || true
    echo "✓ Man page installed (try 'man cmd-genie' or 'man wish')"
else
    # If system-wide installation fails, install to the user's local directory.
    mkdir -p ~/.local/share/man/man1
    cp "$SCRIPT_DIR/cmd-genie.1" ~/.local/share/man/man1/
    ln -sf ~/.local/share/man/man1/cmd-genie.1 ~/.local/share/man/man1/wish.1
    echo "✓ Man page installed to user directory"
    echo "  Note: Add ~/.local/share/man to MANPATH if needed"
fi

# Add a line to the user's .bashrc to source the `x_function.sh` script.
# This makes the `wish` function available in new terminal sessions.
if ! grep -q "# cmd-genie - Wish Terminal Helper" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# cmd-genie - Wish Terminal Helper" >> ~/.bashrc
    echo "source $SCRIPT_DIR/x_function.sh" >> ~/.bashrc
    echo "✓ Added wish function to ~/.bashrc"
else
    echo "✓ wish function already in ~/.bashrc"
fi

# Final instructions for the user.
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