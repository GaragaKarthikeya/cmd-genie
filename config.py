#!/usr/bin/env python3
"""
cmd-genie Configuration File.

This file centralizes all configuration for the cmd-genie application,
allowing for easy customization of AI settings, display properties, prompt
templates, and other operational behaviors.
"""

# =============================================================================
# AI Configuration
# =============================================================================
# This section governs the behavior of the Google Gemini AI model.
# =============================================================================

# Gemini API Settings
AI_MODEL = "gemini-2.5-flash-lite"  # The specific Gemini model to use.
COMMAND_TEMPERATURE = 0.0           # Range: 0.0-1.0. Low temp for precise, predictable commands.
DESCRIPTION_TEMPERATURE = 0.3       # Higher temp for more creative, human-like descriptions.
MAX_COMMAND_TOKENS = 100            # Max length of the generated command.
MAX_DESCRIPTION_TOKENS = 200        # Max length of the command's description.

# Rate limiting (to avoid quota issues)
REQUEST_DELAY = 0  # Seconds to wait between consecutive API calls.

# =============================================================================
# Display Configuration
# =============================================================================
# This section defines the visual elements of the command-line interface.
# =============================================================================

# ANSI Color Codes for terminal output.
class Colors:
    """A container for ANSI color codes to style terminal output."""
    # Basic colors
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'

    # Text formatting styles
    BOLD = '\033[1m]'         # Bold text
    DIM = '\033[2m'           # Dim text
    UNDERLINE = '\033[4m'     # Underlined text
    RESET = '\033[0m'         # Reset all formatting

    # Semantic theme colors for cmd-genie's output
    PURPOSE = f'{BOLD}{CYAN}'      # Color for the "Purpose" section of the description
    FLAGS = f'{BOLD}{YELLOW}'      # Color for the "Flags" section
    TIP = f'{BOLD}{GREEN}'         # Color for the "Tip" section
    LOADING = f'{DIM}{MAGENTA}'    # Color for the "Conjuring..." loading message
    ERROR = f'{BOLD}{RED}'         # Color for error messages

# Static messages displayed to the user.
LOADING_MESSAGE = "Conjuring..."
REVEAL_MESSAGE = "Press ↑ to reveal"
STARTUP_MESSAGE = "Ready to grant wishes"

# =============================================================================
# AI Prompts Configuration
# =============================================================================
# These templates guide the AI in generating commands and descriptions.
# =============================================================================

# The template for generating the Linux command.
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

# The template for generating the command's description.
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
# Settings to prevent the execution of potentially harmful commands.
# =============================================================================

# A list of regex patterns for commands that should be blocked.
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/\s*$',      # 'rm -rf /' (root deletion)
    r':\(\)\{.*\}.*:',         # Fork bombs
    r'mkfs\.',                 # Formatting commands
    r'dd\s+.*of=/dev/',        # Dangerous 'dd' operations
    r'chmod\s+-R\s+777\s+/',   # Dangerous permission changes
]

# A safeguard against excessively long or malformed commands.
MAX_COMMAND_LENGTH = 200

# =============================================================================
# Feature Flags
# =============================================================================
# Toggles to enable or disable specific features of the application.
# =============================================================================

ENABLE_COLORS = True           # Show colored output.
ENABLE_MARKDOWN = True         # Use structured markdown for descriptions.
ENABLE_GENIE_PERSONALITY = True  # Include subtle genie-like language.
ENABLE_SAFETY_CHECKS = True    # Block commands matching DANGEROUS_PATTERNS.
ENABLE_COMMAND_HISTORY = True  # Add successfully generated commands to bash history.

# Debug settings
DEBUG_MODE = False             # Show additional debug information.
VERBOSE_ERRORS = False         # Show detailed error messages for troubleshooting.

# =============================================================================
# File Paths
# =============================================================================
# Defines the locations for temporary files used by the application.
# =============================================================================

TEMP_COMMAND_FILE = "/tmp/wish_cmd"  # File to store the last generated command.
LOG_FILE = "/tmp/cmd-genie.log"      # File for logging application events.

# =============================================================================
# Error Messages
# =============================================================================
# A dictionary of user-facing error messages and corresponding fallback commands.
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
# Utility functions used throughout the application.
# =============================================================================

def get_color(color_name):
    """
    Retrieves an ANSI color code from the Colors class by its name.

    This function fetches the specified color code, but returns an empty string
    if the ENABLE_COLORS feature flag is set to False.

    Args:
        color_name (str): The name of the color to retrieve (e.g., 'CYAN').

    Returns:
        str: The ANSI color code, or an empty string if colors are disabled.
    """
    if not ENABLE_COLORS:
        return ''
    return getattr(Colors, color_name.upper(), '')

def format_colored_text(text, color_name):
    """
    Applies ANSI color formatting to a string of text.

    If colors are disabled via the ENABLE_COLORS flag, this function returns
    the original text without modification.

    Args:
        text (str): The text to be colored.
        color_name (str): The name of the color to apply.

    Returns:
        str: The color-formatted text, or the original text if colors are off.
    """
    if not ENABLE_COLORS:
        return text
    color = get_color(color_name)
    reset = Colors.RESET
    return f"{color}{text}{reset}"