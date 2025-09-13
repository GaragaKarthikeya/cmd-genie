#!/bin/bash
# 🧞‍♂️ cmd-genie - Your Magical Linux Command Assistant
# Rub the lamp (type 'wish') and make your command wishes come true!

# Colors for output
readonly X_GREEN='\033[0;32m'
readonly X_BLUE='\033[0;34m' 
readonly X_YELLOW='\033[1;33m'
readonly X_CYAN='\033[0;36m'
readonly X_RED='\033[0;31m'
readonly X_BOLD='\033[1m'
readonly X_RESET='\033[0m'

# The magic function
wish() {
    if [ $# -eq 0 ]; then
        echo -e "${X_YELLOW}What would you like to accomplish?${X_RESET}"
        echo -e "${X_CYAN}Example:${X_RESET} wish 'list all files'"
        return 1
    fi
    
    # Show loading indicator
    echo -e "${X_BLUE}Conjuring...${X_RESET}"
    
    # Call Python backend
    local result=$(python3 "/home/obsidian-core/cmd-genie/x_backend.py" "$@" 2>/dev/null)
    
    if [ $? -ne 0 ] || [ -z "$result" ]; then
        echo -e "${X_RED}Unable to process request${X_RESET}"
        echo -e "${X_CYAN}Check configuration: export GEMINI_API_KEY='your-key'${X_RESET}"
        return 1
    fi
    
    # Parse result (last line = command, everything else = explanation)
    local command=$(echo "$result" | tail -n1)
    local explanation=$(echo "$result" | head -n -1)
    
    # Clear loading line
    printf '\033[1A\033[2K'
    
    # Print clean, elegant output
    echo -e "${explanation}"
    echo -e "${X_CYAN}Press ↑ to reveal${X_RESET}"
    
    # Add to history for up arrow access
    history -s "$command"
    
    # Store command for alternative access
    echo "$command" > /tmp/wish_cmd
}

# Export the function
export -f wish

# Genie health check and startup message
genie_startup() {
    local issues=0
    local messages=""
    
    # Check if Python backend exists
    if [ ! -f "/home/obsidian-core/cmd-genie/x_backend.py" ]; then
        messages="${messages}• Backend missing\n"
        ((issues++))
    fi
    
    # Check if Python 3 is available
    if ! command -v python3 >/dev/null 2>&1; then
        messages="${messages}• Python 3 not found\n"
        ((issues++))
    fi
    
    # Check if API key is set
    if [ -z "$GEMINI_API_KEY" ]; then
        messages="${messages}• GEMINI_API_KEY not set\n"
        ((issues++))
    fi
    
    # Check if google-genai is installed
    if ! python3 -c "import google.genai" 2>/dev/null; then
        messages="${messages}• google-genai package missing\n"
        ((issues++))
    fi
    
    if [ $issues -eq 0 ]; then
        echo -e "${X_GREEN}Ready to grant wishes${X_RESET}"
    else
        echo -e "${X_RED}Configuration required:${X_RESET}"
        echo -e "$messages"
        echo -e "${X_YELLOW}Run the install script to resolve${X_RESET}"
    fi
}

# Run startup check
genie_startup