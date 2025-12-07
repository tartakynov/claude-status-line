#!/usr/bin/env python3
import json
import sys
import os

def colorize(text, color):
    """Render text with ANSI color codes.

    Args:
        text: The text to colorize
        color: Color name (red, green, yellow, blue, magenta, cyan, white)

    Returns:
        Text wrapped in ANSI color codes
    """
    colors = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
    }

    color_code = colors.get(color.lower(), 37)  # default to white
    return f"\033[{color_code}m{text}\033[0m"


def estimate_context_length(transcript_path):
    """Estimate the context length from the transcript file.

    Reads the transcript file and extracts token usage information from the last
    usage entry. Sums input tokens, cache read tokens, and cache creation tokens.

    Args:
        transcript_path: Path to the transcript file

    Returns:
        Total context length in tokens (0 if file doesn't exist or no usage data found)
    """
    if not os.path.exists(transcript_path):
        return 0

    try:
        context_length = 0
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                    usage = data.get('usage', {})
                    if not usage and 'message' in data and isinstance(data['message'], dict):
                        usage = data['message'].get('usage', {})

                    if usage:
                        input_tokens = usage.get('input_tokens', 0)
                        cache_read_input_tokens = usage.get('cache_read_input_tokens', 0)
                        cache_creation_input_tokens = usage.get('cache_creation_input_tokens', 0)
                        context_length = input_tokens + cache_read_input_tokens + cache_creation_input_tokens
                except (json.JSONDecodeError, ValueError, TypeError):
                    continue
        return context_length
    except:
        pass

    return None


def get_git_branch():
    """Get the current git branch name.

    Reads the .git/HEAD file to determine the current branch.

    Returns:
        Branch name as a string, or None if not in a git repo or on detached HEAD
    """
    if not os.path.exists('.git'):
        return None

    try:
        with open('.git/HEAD', 'r') as f:
            ref = f.read().strip()
            if ref.startswith('ref: refs/heads/'):
                return ref.replace('ref: refs/heads/', '')
    except:
        pass

    return None


def main():
    # Read JSON from stdin
    data = json.load(sys.stdin)

    # Extract values
    model = data['model']['display_name']
    current_dir = os.path.basename(data['workspace']['current_dir'])
    total_cost_usd = data['cost']['total_cost_usd'] or 0.0
    context_length = estimate_context_length(data['transcript_path'])
    branch = get_git_branch()

    stats = []

    # model
    stats.append(f"🤖 {model}")

    # current dir
    stats.append(f"📁 {colorize(current_dir, 'magenta')}")

    # git branch
    if branch:
        stats.append(f"🌿 {colorize(branch, 'yellow')}")

    # context size
    if context_length is not None:
        stats.append(f"{int(context_length / 1000)}K tokens")

    # cost
    stats.append(f"💰 ${total_cost_usd:.2f}")

    print(' | '.join(stats))

if __name__ == "__main__":
    main()