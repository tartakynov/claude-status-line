# Claude Code Status Line

A single-file status line that doesn't require running shell scripts from random people on the internet. Just one Python file you can review yourself before using.

Displays the estimated context size of your current Claude Code session in the status line, helping you manage your context size and staying in the smart zone.

## What It Displays

The status line shows the following information separated by `|`:

1. **Model**: The current Claude model (e.g., `🤖 Sonnet 4.5`)
2. **Directory**: Current working directory name (in magenta)
3. **Git Branch**: Current git branch if in a git repository (e.g., `🌿 main` in yellow)
4. **Context Size**: Estimated context length in thousands of tokens (e.g., `context length: 42K tokens`)
5. **Cost**: Total session cost (e.g., `💰 $0.15`)

Example output:
```
🤖 Sonnet 4.5 | 📁 claude-status-line | 🌿 main | context length: 42K tokens | 💰 $0.15
```

## Installation

1. Review the `statusline.py` script to ensure it meets your security standards
2. Configure Claude Code to use this script as your status line (instructions in Claude Code documentation)
