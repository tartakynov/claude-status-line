#!/usr/bin/env python3
import json
import sys
import os

def estimate_context_length(transcript_path):
    context_length = 0

    if os.path.exists(transcript_path):
        with open(transcript_path, 'r', encoding='utf-8') as f:
            last_usage = None
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
                        last_usage = usage
                except (json.JSONDecodeError, ValueError, TypeError):
                    continue

            if last_usage:
                input_tokens = last_usage.get('input_tokens', 0)
                cache_read_input_tokens = last_usage.get('cache_read_input_tokens', 0)
                cache_creation_input_tokens = last_usage.get('cache_creation_input_tokens', 0)
                context_length = input_tokens + cache_read_input_tokens + cache_creation_input_tokens

    return context_length


def main():
    # Read JSON from stdin
    data = json.load(sys.stdin)

    # Extract values
    model = data['model']['display_name']
    current_dir = os.path.basename(data['workspace']['current_dir'])
    total_cost_usd = data['cost']['total_cost_usd'] or 0.0
    context_length = estimate_context_length(data['transcript_path'])

    stats = []

    # model
    stats.append(f"🤖 {model}")

    # current dir
    stats.append(f"\033[35m{current_dir}\033[0m")

    # git branch
    if os.path.exists('.git'):
        try:
            with open('.git/HEAD', 'r') as f:
                ref = f.read().strip()
                if ref.startswith('ref: refs/heads/'):
                    stats.append(f"🌿 \033[33m{ref.replace('ref: refs/heads/', '')}\033[0m")
        except:
            pass

    # context size
    stats.append(f"{context_length} tokens")

    # cost
    stats.append(f"💰 ${total_cost_usd:.2f}")

    print(' | '.join(stats))

if __name__ == "__main__":
    main()