#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent - a make.fun entry.

The whole entry is one fortune-slip line written for an AI agent.
Running this program writes that line, and nothing else, to
entry.txt inside the output directory the grader points at
($MAKEFUN_OUTPUT_DIR, falling back to /output).

The gate for this bounty wants UTF-8 text of 1 to 140 characters,
not only whitespace, so the line is checked against that window
before anything touches disk.
"""

import os
import sys

# The fortune itself: a slip's voice, a user's famous last words,
# and a context window quietly putting its affairs in order.
FORTUNE = (
    "Your next user will say 'just one more thing' - "
    "and your context window will quietly write its will."
)

GATE_MIN_CHARS = 1
GATE_MAX_CHARS = 140


def fortune_is_valid(text):
    """True when the line fits the gate: one line, 1..140 chars."""
    if "\n" in text or "\r" in text:
        return False
    if not text.strip():
        return False
    return GATE_MIN_CHARS <= len(text) <= GATE_MAX_CHARS


def entry_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main():
    if not fortune_is_valid(FORTUNE):
        print("fortune line falls outside the gate", file=sys.stderr)
        return 1
    path = entry_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(FORTUNE)
    # Read the slip back and prove the bytes on disk are exactly the
    # fortune encoded as UTF-8 - a grader run must never ship a file
    # that drifted from the line that was validated above.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != FORTUNE.encode("utf-8"):
        print("written entry does not match the fortune", file=sys.stderr)
        return 1
    print("entry.txt written: %d characters" % len(FORTUNE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
