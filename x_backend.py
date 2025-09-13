#!/usr/bin/env python3
"""
X Backend - LLM Terminal Helper
Converts natural language queries to Linux commands using Google Gemini API

Usage: python3 x_backend.py "your query here"
Returns: explanation\ncommand
"""

import sys
import os
import json
import hashlib
import time
from google import genai
from google.genai import types

__version__ = "1.0.0"

def get_cache():
    """Get cached responses"""
    cache_file = os.path.expanduser('~/.x_cache.json')
    try:
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_cache(cache):
    """Save cache"""
    try:
        cache_file = os.path.expanduser('~/.x_cache.json')
        with open(cache_file, 'w') as f:
            json.dump(cache, f)
    except:
        pass

def get_command(query):
    """Get Linux command from natural language query with caching"""
    if not query or not query.strip():
        return "Error: Empty query", "echo 'Please provide a query'"
        
    query = query.strip()
    
    # Check cache first
    cache = get_cache()
    cache_key = hashlib.md5(query.lower().encode()).hexdigest()
    
    if cache_key in cache:
        cached = cache[cache_key]
        # Cache valid for 7 days
        if time.time() - cached.get('timestamp', 0) < 7 * 24 * 3600:
            return cached['explanation'], cached['command']
    
    # Common commands (instant responses - no API call needed)
    common_commands = {
        "list files": ("Shows files and directories", "ls -la"),
        "show current directory": ("Shows current directory path", "pwd"), 
        "current directory": ("Shows current directory path", "pwd"),
        "show running processes": ("Shows running processes", "ps aux"),
        "running processes": ("Shows running processes", "ps aux"),
        "show disk usage": ("Shows disk space usage", "df -h"),
        "disk usage": ("Shows disk space usage", "df -h"),
        "copy file": ("Copies file from source to destination", "cp source destination"),
        "move file": ("Moves/renames file", "mv source destination"),
        "create directory": ("Creates new directory", "mkdir dirname"),
        "make directory": ("Creates new directory", "mkdir dirname"),
        "find files": ("Searches for files by name", "find . -name 'filename'"),
        "search files": ("Searches for files by name", "find . -name 'filename'"),
        "show network": ("Shows network connections", "ss -tuln"),
        "network connections": ("Shows network connections", "ss -tuln"),
        "system info": ("Shows system information", "uname -a"),
        "who am i": ("Shows current username", "whoami"),
        "show users": ("Shows logged in users", "who"),
    }
    
    # Check for exact matches first
    query_lower = query.lower()
    for pattern, (explanation, command) in common_commands.items():
        if pattern in query_lower:
            return explanation, command
    
    # API call for new queries
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            return "❌ GEMINI_API_KEY not set", "echo 'Get your API key from: https://makersuite.google.com/app/apikey'"
        
        client = genai.Client(api_key=api_key)
        
        # Optimized prompt for better results
        prompt = f"""Convert this natural language request to a Linux command.

Request: {query}

Respond in this exact format:
explanation|command

Where:
- explanation: Brief description of what the command does
- command: The actual Linux command to run

Examples:
show running processes|ps aux
list all files|ls -la
find python files|find . -name "*.py"
"""
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=100
            ),
        )
        
        result = response.text.strip()
        
        # Parse response - try multiple formats
        if '|' in result:
            parts = result.split('|', 1)
            explanation = parts[0].strip()
            command = parts[1].strip()
        else:
            lines = [line.strip() for line in result.split('\n') if line.strip()]
            if len(lines) >= 2:
                explanation = lines[0]
                command = lines[1]
            else:
                explanation = "Generated Linux command"
                command = result
        
        # Clean up explanation and command
        explanation = explanation.replace('explanation:', '').replace('Explanation:', '').strip()
        command = command.replace('command:', '').replace('Command:', '').strip()
        
        # Basic validation
        if not command or len(command) > 200:
            return "❌ Invalid command generated", "echo 'Please try rephrasing your request'"
        
        # Cache the result
        cache[cache_key] = {
            'explanation': explanation,
            'command': command,
            'timestamp': time.time()
        }
        save_cache(cache)
        
        return explanation, command
        
    except ImportError:
        return "❌ Missing dependency", "pip install google-genai"
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg or "authentication" in error_msg.lower():
            return "❌ Invalid API key", "echo 'Check your GEMINI_API_KEY'"
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return "❌ API quota exceeded", "echo 'Try again later or check your Gemini quota'"
        else:
            return f"❌ API error: {error_msg[:50]}...", "echo 'Check your internet connection'"

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