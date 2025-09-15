#!/usr/bin/env python3
"""
cmd-genie Backend.

This script serves as the backend for cmd-genie, handling the logic for
transforming natural language queries into Linux commands using the Google
Gemini AI. It is called by the `wish` shell function.

Usage:
    python3 x_backend.py "your wish here"

Returns:
    A string containing the command explanation, followed by a newline,
    and then the generated command.
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
    """
    Renders a structured markdown description with ANSI colors.

    If ENABLE_MARKDOWN is False, it returns the plain text. Otherwise, it
    parses a description with "Purpose:", "Flags:", and "Tip:" sections,
    applies colors from the config, and returns the formatted string.

    Args:
        description_text (str): The markdown-formatted text to render.

    Returns:
        str: The colorized description or plain text if rendering fails or
             is disabled.
    """
    if not ENABLE_MARKDOWN:
        return description_text.strip()

    try:
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
                formatted_parts.append(line)

        if not any('Purpose:' in part or 'Flags:' in part or 'Tip:' in part for part in formatted_parts):
            return description_text.strip()

        return '\n'.join(formatted_parts)

    except Exception:
        return description_text.strip()

def get_command(query):
    """
    Generates a Linux command and its description from a natural language query.

    This function sends two requests to the Gemini API: one to generate a
    precise command (low temperature) and another for a creative explanation
    (higher temperature). It includes basic validation and error handling.

    Args:
        query (str): The user's natural language request.

    Returns:
        tuple: A tuple containing the formatted explanation (str) and the
               generated command (str). In case of an error, returns a tuple
               from ERROR_MESSAGES.

    Raises:
        ImportError: If the `google-genai` library is not installed.
        Exception: Catches and handles various exceptions related to API keys,
                   quotas, and network connections, returning a user-friendly
                   error message from the `ERROR_MESSAGES` dictionary.
    """
    if not query or not query.strip():
        return ERROR_MESSAGES['no_query']

    query = query.strip()

    if REQUEST_DELAY > 0:
        time.sleep(REQUEST_DELAY)

    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return ERROR_MESSAGES['no_api_key']

        client = genai.Client(api_key=api_key)

        command_prompt = COMMAND_PROMPT_TEMPLATE.format(query=query)
        command_response = client.models.generate_content(
            model=AI_MODEL,
            contents=command_prompt,
            config=types.GenerateContentConfig(
                temperature=COMMAND_TEMPERATURE,
                max_output_tokens=MAX_COMMAND_TOKENS
            ),
        )

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

        command = command_response.text.strip()
        explanation = description_response.text.strip()

        def validate_and_clean(desc, cmd):
            """
            Performs validation and cleaning on the AI-generated output.

            This function strips whitespace, removes common prefixes and wrapping
            quotes/backticks from the command, and checks against a list of
            dangerous command patterns defined in the configuration.

            Args:
                desc (str): The AI-generated description of the command.
                cmd (str): The AI-generated command string.

            Returns:
                tuple: A tuple containing the cleaned description and command.
                       Returns (None, None) if the command is invalid or unsafe.
            """
            import re

            # Standardize description if it's empty or a placeholder.
            desc = desc.strip()
            if not desc or desc.lower() in ['description', 'explanation', 'desc']:
                desc = "Generated command"

            # Clean the command string.
            cmd = cmd.strip()
            if not cmd:
                return None, None

            # Remove potential wrapping characters and prefixes.
            cmd = re.sub(r'^["\'](.+)["\']$', r'\1', cmd)
            cmd = re.sub(r'^`(.+)`$', r'\1', cmd)
            cmd = re.sub(r'^(command|cmd):\s*', '', cmd, flags=re.IGNORECASE)

            # Block command if it matches any dangerous patterns.
            if ENABLE_SAFETY_CHECKS:
                for pattern in DANGEROUS_PATTERNS:
                    if re.search(pattern, cmd, re.IGNORECASE):
                        return None, None

            # Enforce maximum command length.
            if len(cmd) > MAX_COMMAND_LENGTH:
                return None, None

            return desc, cmd

        explanation, command = validate_and_clean(explanation, command)

        if not explanation or not command:
            return ERROR_MESSAGES['processing_failed']

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
    """
    Handles the script's execution from the command line.

    This function serves as the main entry point when the script is run
    directly. It parses the command-line arguments to get the user's query,
    calls `get_command` to process it, and then prints the explanation and
    command to standard output. This output is then captured by the `wish`
    shell function.

    Side Effects:
        - Prints usage information and exits if no query is provided.
        - Prints the final explanation and command to stdout.
    """
    if len(sys.argv) < 2:
        print("Usage: x_backend.py 'query'")
        sys.exit(1)

    query = ' '.join(sys.argv[1:])
    explanation, command = get_command(query)

    # The output is printed in a specific format (explanation, newline, command)
    # to be easily parsed by the calling shell script.
    print(explanation)
    print(command)

if __name__ == "__main__":
    main()