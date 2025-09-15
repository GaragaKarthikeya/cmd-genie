#!/bin/bash
#
# cmd-genie - Your Magical Linux Command Assistant
# This script defines the `wish` shell function, which is the primary
# interface for the user to interact with cmd-genie.
#

# Define ANSI color codes for styled output.
readonly X_GREEN='\033[0;32m'
readonly X_BLUE='\033[0;34m'
readonly X_YELLOW='\033[1;33m'
readonly X_CYAN='\033[0;36m'
readonly X_RED='\033[0;31m'
readonly X_BOLD='\033[1m'
readonly X_RESET='\033[0m'

##
# The main `wish` function that processes user requests.
#
# This function serves as the primary entry point for the user. It takes a
# natural language string as an argument, sends it to the Python backend for
# processing, and displays the AI-generated command and description.
#
# ## Arguments:
#   $@ - The user's natural language request as a string.
#
# ## Outputs:
#   - Prints the AI-generated description to stdout.
#   - Injects the AI-generated command into the shell's history.
#
wish() {
    # If no arguments are provided, show a usage example and exit.
    if [ $# -eq 0 ]; then
        echo -e "${X_YELLOW}What would you like to accomplish?${X_RESET}"
        echo -e "${X_CYAN}Example:${X_RESET} wish 'list all files'"
        return 1
    fi
    
    # Display a loading indicator to the user.
    echo -e "${X_BLUE}Conjuring...${X_RESET}"
    
    # Determine the script's directory to dynamically locate the backend.
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
    
    # Call the Python backend, passing all arguments to it.
    local result
    result=$(python3 "$script_dir/x_backend.py" "$@" 2>/dev/null)

    # Check for errors from the backend script.
    if [ $? -ne 0 ] || [ -z "$result" ]; then
        echo -e "${X_RED}Unable to process request${X_RESET}"
        echo -e "${X_CYAN}Check configuration: export GEMINI_API_KEY='your-key'${X_RESET}"
        return 1
    fi
    
    # The command is the last line of the backend's output.
    local command
    command=$(echo "$result" | tail -n1)

    # The explanation is everything before the last line.
    local explanation
    explanation=$(echo "$result" | head -n -1)
    
    # Clear the "Conjuring..." line from the terminal.
    printf '\033[1A\033[2K'
    
    # Print the formatted explanation and the reveal prompt.
    echo -e "${explanation}"
    echo -e "${X_CYAN}Press ↑ to reveal${X_RESET}"
    
    # Add the command to shell history for easy access with the up arrow.
    history -s "$command"
    
    # Store the command in a temporary file for other potential integrations.
    echo "$command" > /tmp/wish_cmd
}

# Make the `wish` function available to sub-shells.
export -f wish

##
# Performs a health check to ensure cmd-genie is configured correctly.
#
# This function is executed when the script is sourced. It checks for common
# configuration issues (e.g., missing dependencies, API key) and provides
# guidance to the user if any problems are found.
#
# ## Outputs:
#   - Prints a success message or a list of configuration issues to stdout.
#
genie_startup() {
    local issues=0
    local messages=""
    
    local script_dir
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

    # Check 1: Ensure the Python backend script is present.
    if [ ! -f "$script_dir/x_backend.py" ]; then
        messages="${messages}• Backend missing\n"
        ((issues++))
    fi
    
    # Check 2: Verify that Python 3 is installed and in the PATH.
    if ! command -v python3 >/dev/null 2>&1; then
        messages="${messages}• Python 3 not found\n"
        ((issues++))
    fi
    
    # Check 3: Confirm that the user has set their Gemini API key.
    if [ -z "$GEMINI_API_KEY" ]; then
        messages="${messages}• GEMINI_API_KEY not set\n"
        ((issues++))
    fi
    
    # Check 4: Ensure the required 'google-genai' Python package is installed.
    if ! python3 -c "import google.genai" 2>/dev/null; then
        messages="${messages}• google-genai package missing\n"
        ((issues++))
    fi
    
    # If any issues were found, print them; otherwise, show a success message.
    if [ $issues -eq 0 ]; then
        echo -e "${X_GREEN}Ready to grant wishes${X_RESET}"
    else
        echo -e "${X_RED}Configuration required:${X_RESET}"
        echo -e "$messages"
        echo -e "${X_YELLOW}Run the install script to resolve${X_RESET}"
    fi
}

# Run the startup health check when the script is sourced.
genie_startup