#!/bin/bash
# 🧞‍♂️ cmd-genie - Your Magical Linux Command Assistant
# Rub the lamp (type 'x') and make your command wishes come true!

# Colors for output
readonly X_GREEN='\033[0;32m'
readonly X_BLUE='\033[0;34m' 
readonly X_YELLOW='\033[1;33m'
readonly X_CYAN='\033[0;36m'
readonly X_RED='\033[0;31m'
readonly X_BOLD='\033[1m'
readonly X_RESET='\033[0m'

# The magic function
x() {
    if [ $# -eq 0 ]; then
        echo -e "${X_YELLOW}Usage:${X_RESET} x 'your natural language query'"
        echo -e "${X_CYAN}Example:${X_RESET} x 'list all files'"
        return 1
    fi
    
    # Show loading indicator
    echo -e "${X_BLUE}�‍♂️ Granting your wish...${X_RESET}"
    
    # Call Python backend
    local result=$(python3 "/home/obsidian-core/llm_cmd_helper/x_backend.py" "$@" 2>/dev/null)
    
    if [ $? -ne 0 ] || [ -z "$result" ]; then
        echo -e "${X_RED}❌ Error: Could not get command${X_RESET}"
        echo -e "${X_CYAN}💡 Check your API key: export GEMINI_API_KEY='your-key'${X_RESET}"
        return 1
    fi
    
    # Parse result (first line = explanation, second line = command)
    local explanation=$(echo "$result" | head -n1)
    local command=$(echo "$result" | tail -n1)
    
    # Clear loading line
    printf '\033[1A\033[2K'
    
    # Print explanation with icon
    echo -e "${X_GREEN}💡 ${explanation}${X_RESET}"
    
    # Add to history for up arrow access
    history -s "$command"
    
    # Store command for alternative access
    echo "$command" > /tmp/x_cmd
    
    # Print the command with nice formatting
    echo -e "${X_BOLD}╭─ Command ready:${X_RESET}"
    echo -e "${X_BOLD}│${X_RESET}  ${X_CYAN}${command}${X_RESET}"
    echo -e "${X_BOLD}╰─${X_RESET} ${X_YELLOW}Press ↑ (up arrow) to use${X_RESET}"
}

# Export the function
export -f x

echo "🧞‍♂️ cmd-genie is ready! Make a wish: x 'list files'"