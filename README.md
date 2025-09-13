# 🤖 X - LLM Terminal Helper

**AI-powered Linux command assistant that speaks your language**

Transform natural language into Linux commands instantly. No more googling, no more man pages - just ask and execute.

```bash
$ x "show running processes"
💡 Shows running processes
╭─ Command ready:
│  ps aux  
╰─ Press ↑ (up arrow) to use

$ x "find files named config"  
💡 Searches for files by name pattern
╭─ Command ready:  
│  find . -name "*config*"
╰─ Press ↑ (up arrow) to use
```

## ✨ Features

- **🎯 Smart**: Powered by Google Gemini AI for accurate command suggestions
- **⚡ Fast**: Common commands cached locally for instant responses  
- **🛡️ Safe**: Always shows you the command before execution
- **🎨 Beautiful**: Colorful output with helpful explanations
- **📚 Learning**: Builds your command history as you use it

## 🚀 Installation

1. **Get a Gemini API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Install X**:
   ```bash
   git clone https://github.com/yourusername/llm_cmd_helper
   cd llm_cmd_helper
   ./install.sh
   ```
3. **Set your API key**:
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   # Add to ~/.bashrc to make permanent
   echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
   ```
4. **Start using**: Open new terminal and try `x "list files"`

## 📚 Examples

```bash
# File operations
x "list all files with details"           # → ls -la
x "find all python files"                 # → find . -name "*.py"  
x "compress current directory"             # → tar -czf backup.tar.gz .

# System monitoring  
x "show running processes"                 # → ps aux
x "check disk space"                       # → df -h
x "monitor system resources"               # → top

# Text processing
x "search for text in files"              # → grep -r "pattern" .
x "count lines in file"                    # → wc -l filename
x "show last 50 log entries"              # → tail -n 50 /var/log/syslog

# Network & system
x "show network connections"               # → ss -tuln  
x "check who's logged in"                  # → who
x "show system information"                # → uname -a
```

## ⚙️ How It Works

1. **Ask**: `x "what you want to do"`
2. **AI thinks**: Gemini converts your request to Linux command
3. **Preview**: See explanation + command with beautiful formatting  
4. **Execute**: Press ↑ (up arrow) to load command, then Enter to run
5. **Learn**: Command saved in history for future reference

## 💻 Requirements

- **Python 3.9+** - Modern Python installation
- **Bash shell** - Standard on most Linux systems  
- **Google Gemini API key** - Free from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Internet connection** - For AI-powered suggestions

## 📁 Project Structure  

```
llm_cmd_helper/
├── 🐍 x_backend.py      # AI engine (Gemini API integration)
├── 🔧 x_function.sh     # Bash magic (readline integration) 
├── ⚡ install.sh        # One-command setup
├── 📦 requirements.txt  # Dependencies (just google-genai)
└── 📖 README.md         # You are here
```

## 🔧 Development

```bash
# Test the backend directly
python3 x_backend.py "your query"

# Reload function after changes
source x_function.sh

# Check function is loaded
type x
```

## 🤝 Contributing

Found a bug or want to add a feature? Pull requests welcome!

## 📜 License

MIT License - feel free to modify and distribute!

---

**Made with ❤️ for the Linux community**

*Simple, fast, reliable.*