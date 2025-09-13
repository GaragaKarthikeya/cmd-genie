#!/usr/bin/env python3
"""
cmd-genie Backend - Your Magical Linux Command Assistant 🧞‍♂️
Transforms natural language wishes into perfect Linux commands using Google Gemini AI

Usage: python3 x_backend.py "your wish here"
Returns: explanation\ncommand

Make a wish, get the perfect command!
"""

import sys
import os
from google import genai
from google.genai import types

__version__ = "1.0.0"

def get_command(query):
    """Get Linux command from natural language query"""
    if not query or not query.strip():
        return "Please provide a request", "echo 'Specify what you would like to accomplish'"
        
    query = query.strip()
    
    # Always use AI - no cached commands
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return "API key required", "echo 'Get your key at https://makersuite.google.com/app/apikey'"
        
        client = genai.Client(api_key=api_key)
        
        # Step 1: Get accurate command with low temperature
        command_prompt = f"""You are a Linux command expert. Generate the most appropriate Linux command for this request.

User request: "{query}"

Respond with ONLY the command, nothing else. Be precise and accurate.

Examples:
- "show running processes" → ps aux
- "find text files" → find . -name "*.txt"
- "check disk space" → df -h
- "what is the time" → date

Command for "{query}":"""
        
        command_response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=command_prompt,
            config=types.GenerateContentConfig(
                temperature=0.0,  # Very low for accuracy
                max_output_tokens=50
            ),
        )
        
        # Step 2: Generate creative description with high temperature
        description_prompt = f"""You are a mystical Linux genie with poetic flair. Create an elegant, sophisticated description for this Linux command.

Command: {command_response.text.strip()}
User's original request: "{query}"

Use mystical, elegant language - words like "reveals", "unveils", "discovers", "summons", "manifests", "conjures". Be creative but not silly.

Examples:
- For "ps aux": "Reveals all active processes dancing within the system's realm"
- For "find . -name '*.txt'": "Discovers hidden text scrolls throughout the current domain"
- For "df -h": "Unveils the sacred allocation of storage across all mounted realms"

Your elegant description:"""
        
        description_response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=description_prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,  # High for creativity
                max_output_tokens=80
            ),
        )
        
        # Combine the results
        command = command_response.text.strip()
        explanation = description_response.text.strip()
        
        # No parsing needed since we have separate command and description
        
        # Minimal validation - trust the AI but basic safety
        def validate_and_clean(desc, cmd):
            """Clean and do minimal validation"""
            import re
            
            # Clean description
            desc = desc.strip()
            if not desc or desc.lower() in ['description', 'explanation', 'desc']:
                desc = "Generated command"
            
            # Clean command
            cmd = cmd.strip()
            if not cmd:
                return None, None
            
            # Remove quotes if command is wrapped
            cmd = re.sub(r'^["\'](.+)["\']$', r'\1', cmd)
            
            # Remove common prefixes
            cmd = re.sub(r'^(command|cmd):\s*', '', cmd, flags=re.IGNORECASE)
            
            # Only block extremely dangerous patterns
            dangerous_patterns = [
                r'rm\s+-rf\s+/\s*$',  # rm -rf / (root deletion)
                r':\(\)\{.*\}.*:',     # fork bombs
                r'mkfs\.',             # format commands
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, cmd, re.IGNORECASE):
                    return None, None
            
            # Basic length check
            if len(cmd) > 500:
                return None, None
            
            return desc, cmd
        
        explanation, command = validate_and_clean(explanation, command)
        
        if not explanation or not command:
            return "Unable to process request", "echo 'Please try a different approach'"
        
        return explanation, command
        
    except ImportError:
        return "Missing dependency", "pip install google-genai"
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg or "authentication" in error_msg.lower():
            return "Authentication failed", "echo 'Verify your GEMINI_API_KEY'"
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return "API quota exceeded", "echo 'Try again later - quota limit reached'"
        else:
            return f"Connection failed", "echo 'Check your internet connection'"

def main():
    if len(sys.argv) < 2:
        print("Usage: x_backend.py 'query'")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    explanation, command = get_command(query)
    
    # Output format for bash function
    print(explanation)
    print(command)

if __name__ == "__main__":
    main()