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

## 📖 Documentation

Access the complete manual anytime:
```bash
man cmd-genie    # Full documentation
man wish         # Same manual, shorter command
```

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

The `wish` command is a Bash function that orchestrates the following steps:

1.  **Input**: You type `wish "your request"` in your terminal.
2.  **Backend Call**: The `wish` function calls the Python script `x_backend.py`, passing your request as an argument.
3.  **Dual AI Generation**: The backend sends two parallel requests to the Google Gemini API:
    *   **Command Generation**: A request with a `temperature` of `0.0` asks the AI for a precise, executable Linux command that matches your request.
    *   **Description Generation**: A second request with a higher `temperature` asks the AI to generate a creative, mystical description of what the command does.
4.  **Parsing and Display**: The Python script returns the description and the command to the Bash function. The `wish` function then:
    *   Displays the mystical explanation.
    *   Prints `Press ↑ to reveal` to the console.
    *   Uses the `history -s` command to inject the generated Linux command into your shell's history.
5.  **Execution**: When you press the **Up Arrow** key, the command appears in your terminal, ready to be edited or executed by pressing **Enter**.

This dual-temperature approach ensures that the commands are accurate and safe, while the descriptions are engaging and educational.

## 💻 Requirements

-   **Python 3.9+**: Required to run the backend script.
-   **Bash Shell**: The `wish` function is a Bash script.
-   **Google Gemini API Key**: Necessary for AI-powered command generation. You can get a free key from [Google AI Studio](https://makersuite.google.com/app/apikey).
-   **Internet Connection**: Required to communicate with the Gemini API.
-   **Color-Enabled Terminal**: Recommended for the best visual experience.

## 📁 Project Structure

```
cmd-genie/
├── x_backend.py        # Main Python backend for AI logic.
├── x_function.sh       # Bash script defining the 'wish' function.
├── install.sh          # Installation script for setup.
├── config.py           # Configuration for AI, prompts, and colors.
├── requirements.txt    # Python dependencies.
└── README.md           # This file.
```

## 🎭 The Genie Experience

cmd-genie is designed to be more than just a utility; it's an experience.

-   **Dual-Temperature AI**: Commands are generated at `temperature = 0.0` for maximum accuracy, while descriptions are generated at `temperature = 0.8` for creativity and flair.
-   **Elegant Loading**: The "Conjuring..." message and the smooth reveal mechanism provide a refined user experience.
-   **Poetic Descriptions**: The explanations are designed to be sophisticated and informative, turning a simple command lookup into a moment of discovery.

## 🔧 Development

If you want to contribute to or modify `cmd-genie`, here are some tips to get you started:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/cmd-genie
    cd cmd-genie
    ```
2.  **Set Up Your Environment**:
    *   Run `./install.sh` to install dependencies and set up the `wish` command.
    *   Make sure to set your `GEMINI_API_KEY` as described in the **Installation** section.
3.  **Making Changes**:
    *   **Backend**: To test changes in the Python backend, you can run it directly:
        ```bash
        python3 x_backend.py "your query"
        ```
    *   **Frontend**: If you modify `x_function.sh`, you'll need to reload it in your current terminal session:
        ```bash
        source x_function.sh
        ```
    *   You can check if the function is loaded correctly with `type wish`.

## ⚙️ Configuration

You can customize the behavior of `cmd-genie` by editing the `config.py` file. This file allows you to change:

-   **AI Settings**: Modify the `AI_MODEL`, `TEMPERATURE`, and `MAX_TOKENS` to fine-tune the AI's responses.
-   **Colors**: Adjust the ANSI color codes in the `Colors` class to match your terminal's theme.
-   **Prompts**: Change the `COMMAND_PROMPT_TEMPLATE` and `DESCRIPTION_PROMPT_TEMPLATE` to alter the AI's personality or output format.
-   **Feature Flags**: Enable or disable features like color output, safety checks, and more.

## 🤝 Contributing

Found a bug or want to add a feature? Pull requests welcome!

## 📜 License

MIT License - feel free to modify and distribute!

---

**Made with ❤️ for the Linux community**

*Your wish is my command* 🧞‍♂️