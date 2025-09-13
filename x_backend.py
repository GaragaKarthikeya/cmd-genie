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
import time
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from config import *

__version__ = "1.0.0"

def render_markdown_description(description_text):
    """Render markdown description beautifully in terminal using config colors"""
    if not ENABLE_MARKDOWN:
        return description_text.strip()
        
    try:
        # Parse the structured response and format it with configured colors
        lines = description_text.strip().split('\n')
        formatted_parts = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('**Purpose:**'):
                purpose = line.replace('**Purpose:**', '').strip()
                formatted_parts.append(f"{Colors.PURPOSE}Purpose:{Colors.RESET} {purpose}")
            elif line.startswith('**Flags:**'):
                flags = line.replace('**Flags:**', '').strip()
                formatted_parts.append(f"{Colors.FLAGS}Flags:{Colors.RESET} {flags}")
            elif line.startswith('**Tip:**'):
                tip = line.replace('**Tip:**', '').strip()
                formatted_parts.append(f"{Colors.TIP}Tip:{Colors.RESET} {tip}")

            elif line and not line.startswith('**'):
                # Handle lines that don't follow the expected format - just return as-is
                formatted_parts.append(line)
        
        # If no structured format found, return original text
        if not any('Purpose:' in part or 'Flags:' in part or 'Tip:' in part for part in formatted_parts):
            return description_text.strip()
        
        # Join the formatted parts
        return '\n'.join(formatted_parts)
        
    except Exception:
        # Fallback to plain text if rendering fails
        return description_text.strip()

def get_command(query):
    """Get Linux command from natural language query"""
    if not query or not query.strip():
        return ERROR_MESSAGES['no_query']
        
    query = query.strip()
    
    # Rate limiting
    if REQUEST_DELAY > 0:
        time.sleep(REQUEST_DELAY)
    
    # Always use AI - no cached commands
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return ERROR_MESSAGES['no_api_key']
        
        client = genai.Client(api_key=api_key)
        
        # Step 1: Get accurate command with low temperature
        command_prompt = COMMAND_PROMPT_TEMPLATE.format(query=query)
        
        command_response = client.models.generate_content(
            model=AI_MODEL,
            contents=command_prompt,
            config=types.GenerateContentConfig(
                temperature=COMMAND_TEMPERATURE,
                max_output_tokens=MAX_COMMAND_TOKENS
            ),
        )
        
        # Step 2: Generate educational description with subtle genie touch
        description_prompt = DESCRIPTION_PROMPT_TEMPLATE.format(
            command=command_response.text.strip(),
            query=query
        )
        
        description_response = client.models.generate_content(
            model=AI_MODEL,
            contents=description_prompt,
            config=types.GenerateContentConfig(
                temperature=DESCRIPTION_TEMPERATURE,
                max_output_tokens=MAX_DESCRIPTION_TOKENS
            ),
        )
        
        # Combine the results
        command = command_response.text.strip()
        explanation = description_response.text.strip()
        
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
            
            # Remove quotes and backticks if command is wrapped
            cmd = re.sub(r'^["\'](.+)["\']$', r'\1', cmd)
            cmd = re.sub(r'^`(.+)`$', r'\1', cmd)
            
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
            return ERROR_MESSAGES['processing_failed']
        
        # Render markdown description beautifully
        formatted_explanation = render_markdown_description(explanation)
        
        return formatted_explanation, command
        
    except ImportError:
        return ERROR_MESSAGES['missing_dependency']
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg or "authentication" in error_msg.lower():
            return ERROR_MESSAGES['auth_failed']
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return ERROR_MESSAGES['quota_exceeded']
        else:
            return ERROR_MESSAGES['connection_failed']

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