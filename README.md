# 🧞‍♂️ cmd-genie

**Your elegant Linux command assistant - make a wish, receive mystical wisdom**

Transform natural language into Linux commands with sophisticated, genie-like descriptions. No more googling, no more man pages - just make a wish and discover the perfect command.️ cmd-genie

**Your magical Linux command assistant - make a wish, get the perfect command**

Transform natural language into Linux commands instantly. No more googling, no more man pages - just make a wish and execute.

```bash
$ wish "show running processes"
Conjuring...
Hark! With 'ps aux', I conjure forth a spectral tapestry, wherein the ethereal forms of every running process are manifest
Press ↑ to reveal

$ wish "what is the time"
Conjuring...
The ethereal chronometer is summoned, unveiling the celestial tapestry of time woven upon the loom of the universe
Press ↑ to reveal
```

## ✨ Features

- **🎯 Smart**: Dual-temperature AI system for precise commands and creative descriptions
- **🧙‍♂️ Mystical**: Elegant genie personality with poetic command explanations
- **⚡ Fast**: Powered by Google Gemini 2.0 Flash for instant responses  
- **🛡️ Safe**: Always shows you the command before execution
- **🎨 Elegant**: Clean, sophisticated UI with mystical loading states
- **📚 Intuitive**: Natural language input with no command syntax to learn

## 🚀 Installation

1. **Get a Gemini API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Install cmd-genie**:
   ```bash
   git clone https://github.com/yourusername/cmd-genie
   cd cmd-genie
   ./install.sh
   ```
3. **Set your API key**:
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   # Add to ~/.bashrc to make permanent
   echo 'export GEMINI_API_KEY="your-key"' >> ~/.bashrc
   ```
4. **Start using**: Open new terminal and try `wish "list files"`

## 📚 Examples

```bash
# File operations
wish "list all files with details"           # → ls -la
wish "find all python files"                 # → find . -name "*.py"  
wish "compress current directory"             # → tar -czf backup.tar.gz .

# System monitoring  
wish "show running processes"                 # → ps aux
wish "check disk space"                       # → df -h
wish "monitor system resources"               # → top

# Text processing
wish "search for text in files"              # → grep -r "pattern" .
wish "count lines in file"                    # → wc -l filename
wish "show last 50 log entries"              # → tail -n 50 /var/log/syslog

# Network & system
wish "show network connections"               # → ss -tuln  
wish "check who's logged in"                  # → who
wish "show system information"                # → uname -a

# Time & date
wish "what is the time"                       # → date
wish "show current timestamp"                 # → date +%s
wish "format date as ISO"                     # → date --iso-8601
```

## ⚙️ How It Works

1. **Wish**: `wish "what you want to do"`
2. **AI conjures**: Dual-temperature system generates precise command (temp 0.0) and mystical description (temp 0.8)
3. **Mystical preview**: Elegant loading state followed by poetic command explanation
4. **Execute**: Press ↑ (up arrow) to reveal the actual command, then Enter to run
5. **Learn**: Natural language interface builds intuitive understanding over time

## 💻 Requirements

- **Python 3.9+** - Modern Python installation
- **Bash shell** - Standard on most Linux systems  
- **Google Gemini API key** - Free from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Internet connection** - For dual-temperature AI processing
- **Terminal with color support** - For elegant mystical theming

## 📁 Project Structure  

```
cmd-genie/
├── 🧞‍♂️ x_backend.py      # The genie's brain (dual-temperature AI processing)
├── 🔧 x_function.sh     # Magic lamp (elegant bash integration) 
├── ⚡ install.sh        # Summon the genie (one-command setup)
├── 📦 requirements.txt  # Genie's requirements (just google-genai)
└── 📖 README.md         # You are here
```

## 🎭 The Genie Experience

cmd-genie combines technical precision with mystical elegance:

- **Dual-Temperature AI**: Commands generated at temperature 0.0 for accuracy, descriptions at 0.8 for creativity
- **Elegant Loading**: "Conjuring..." state with smooth reveal mechanism  
- **Poetic Descriptions**: Sophisticated, genie-like explanations that are informative yet mystical
- **Clean UX**: No flashy animations or gimmicky elements - just refined, purposeful design
- **Robust Parsing**: Handles various AI response formats with comprehensive regex patterns

## 🔧 Development

```bash
# Test the backend directly
python3 x_backend.py "your query"

# Reload function after changes
source x_function.sh

# Check function is loaded
type wish
```

## 🤝 Contributing

Found a bug or want to add a feature? Pull requests welcome!

## 📜 License

MIT License - feel free to modify and distribute!

---

**Made with ❤️ for the Linux community**

*Your wish is my command* 🧞‍♂️