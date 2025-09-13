#!/usr/bin/env python3
"""
cmd-genie Configuration File 🧞‍♂️
Centralized configuration for the magical Linux command assistant

Customize colors, AI settings, prompts, and behavior here.
"""

# =============================================================================
# AI Configuration
# =============================================================================

# Gemini API Settings
AI_MODEL = "gemini-2.5-flash-lite"
COMMAND_TEMPERATURE = 0.0      # Very low for accuracy
DESCRIPTION_TEMPERATURE = 0.3  # Moderate for educational clarity
MAX_COMMAND_TOKENS = 100
MAX_DESCRIPTION_TOKENS = 200

# Rate limiting (to avoid quota issues)
REQUEST_DELAY = 0  # Seconds between API calls

# =============================================================================
# Display Configuration
# =============================================================================

# ANSI Color Codes
class Colors:
    # Basic colors
    CYAN = '\033[96m'
    YELLOW = '\033[93m' 
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    
    # Text formatting
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    # Genie theme colors
    PURPOSE = f'{BOLD}{CYAN}'      # Bright cyan for Purpose
    FLAGS = f'{BOLD}{YELLOW}'      # Bright yellow for Flags  
    TIP = f'{BOLD}{GREEN}'         # Bright green for Tips
    LOADING = f'{DIM}{MAGENTA}'    # Dim magenta for loading
    ERROR = f'{BOLD}{RED}'         # Bright red for errors

# Display Messages
LOADING_MESSAGE = "Conjuring..."
REVEAL_MESSAGE = "Press ↑ to reveal"
STARTUP_MESSAGE = "Ready to grant wishes"

# =============================================================================
# AI Prompts Configuration
# =============================================================================

# Command Generation Prompt
COMMAND_PROMPT_TEMPLATE = """You are a Linux command expert. Provide a COMPLETE, practical command for the user's request.

User request: "{query}"

Respond with ONLY the complete, executable command - no backticks, quotes, or formatting. Make sure the command is fully formed and ready to run.

Examples:
- "show running processes" → ps aux
- "find text files" → find . -name "*.txt"
- "find large files" → find . -type f -size +100M
- "images larger than 10MB" → find . -type f \( -name "*.jpg" -o -name "*.png" \) -size +10M
- "check disk space" → df -h

Complete command for "{query}":"""

# Description Generation Prompt  
DESCRIPTION_PROMPT_TEMPLATE = """You are a knowledgeable Linux genie. Create a SHORT, structured explanation.

Command: {command}
User request: "{query}"

Keep it CONCISE. Use this format:
**Purpose:** [What it does in 4-6 words]
**Flags:** [Key flags, very brief]
**Tip:** [Short practical note]

Examples:
**Purpose:** Shows running processes with details
**Flags:** `a` (all users), `u` (user format)
**Tip:** Pipe to grep for filtering

**Purpose:** Finds PDF files in directory
**Flags:** `-name` (search by filename)
**Tip:** Use wildcards with quotes

Your response:"""

# =============================================================================
# Security Configuration
# =============================================================================

# Dangerous command patterns to block
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/\s*$',  # rm -rf / (root deletion)
    r':\(\)\{.*\}.*:',     # fork bombs
    r'mkfs\.',             # format commands
    r'dd\s+.*of=/dev/',    # dangerous dd operations
    r'chmod\s+-R\s+777\s+/', # dangerous permission changes
]

# Maximum command length (security measure)
MAX_COMMAND_LENGTH = 200

# =============================================================================
# Feature Flags
# =============================================================================

# Enable/disable features
ENABLE_COLORS = True           # Show colored output
ENABLE_MARKDOWN = True         # Use structured markdown descriptions
ENABLE_GENIE_PERSONALITY = True  # Include subtle genie language
ENABLE_SAFETY_CHECKS = True    # Block dangerous commands
ENABLE_COMMAND_HISTORY = True  # Add commands to bash history

# Debug settings
DEBUG_MODE = False             # Show debug information
VERBOSE_ERRORS = False         # Show detailed error messages

# =============================================================================
# File Paths
# =============================================================================

# Temporary files
TEMP_COMMAND_FILE = "/tmp/wish_cmd"
LOG_FILE = "/tmp/cmd-genie.log" 

# =============================================================================
# Error Messages
# =============================================================================

ERROR_MESSAGES = {
    'no_query': ("Please provide a request", "echo 'Specify what you would like to accomplish'"),
    'no_api_key': ("API key required", "echo 'Get your key at https://makersuite.google.com/app/apikey'"),
    'missing_dependency': ("Missing dependency", "pip install google-genai rich"),
    'auth_failed': ("Authentication failed", "echo 'Verify your GEMINI_API_KEY'"), 
    'quota_exceeded': ("API quota exceeded", "echo 'Try again later - quota limit reached'"),
    'connection_failed': ("Connection failed", "echo 'Check your internet connection'"),
    'processing_failed': ("Unable to process request", "echo 'Please try a different approach'"),
    'dangerous_command': ("Command blocked for safety", "echo 'Potentially dangerous operation detected'"),
}

# =============================================================================
# Helper Functions
# =============================================================================

def get_color(color_name):
    """Get color code by name, with fallback if colors disabled"""
    if not ENABLE_COLORS:
        return ''
    return getattr(Colors, color_name.upper(), '')

def format_colored_text(text, color_name):
    """Apply color formatting to text"""
    if not ENABLE_COLORS:
        return text
    color = get_color(color_name)
    reset = Colors.RESET
    return f"{color}{text}{reset}"