#!/usr/bin/env python3
"""Deliver the out-of-tokens error message entry for make.fun.

The competition asks for the error message an AI agent shows when it
runs out of tokens mid-sentence, capped at 140 characters. This
script holds that one message in a single constant, runs it through
the competition's gate before writing anything, and only then places
it in the output file the grader reads.

The order is deliberate: validation first, writing second. If the
message were too long, empty, or split across lines, shipping it
anyway would mean the judges score the wrong text, or score nothing
at all. Failing loudly at the gate is the cheap way to catch that.

The message is 83 characters long. It is written to sound like a
real error — plain, factual, cut off in the middle of a thought —
and then the last clause flips it into a joke: the rest of the
thought has not vanished, it is simply for sale. The agent ran out
of tokens, so it is now charging the reader for the ending.
"""

import os
import sys

# ---------------------------------------------------------------------------
# The submission. This exact string is what the judges score, so no
# refactor of this file may edit, re-wrap, or reword it.
# ---------------------------------------------------------------------------
LINE = (
    "Ran out of tokens mid-sentence. The rest of this thought is available for purchase."
)

# Competition gate: the message has to be one line of 1 to 140 chars.
FLOOR = 1
CEILING = 140

# Where the graded file lands. Overridable for local runs.
OUTPUT_ENV_VAR = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"
OUTPUT_MODE = 0o644


def count_characters(line):
    """Return how many characters the message holds."""
    return len(line)


def fail(message):
    """Abort the run with a clear reason instead of shipping bad output."""
    raise SystemExit(f"entry rejected: {message}")


def check_not_empty(line):
    """The message must say something; a blank line is not an error."""
    if not line.strip():
        fail("line is blank")


def check_single_line(line):
    """A one-line message cannot contain a line break of any kind."""
    if "\n" in line or "\r" in line:
        fail("line must be a single line")


def check_length(line, low, high):
    """The message must sit inside the competition's character gate."""
    size = count_characters(line)
    if size < low or size > high:
        fail(f"line is {size} characters, outside the {low}-{high} gate")
    return size


def validate_line(line, low=FLOOR, high=CEILING):
    """Run every gate check and return the verified character count."""
    check_not_empty(line)
    check_single_line(line)
    return check_length(line, low, high)


def resolve_output_path():
    """Work out the full path of the file the grader will read."""
    directory = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_DIR)
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, OUTPUT_FILENAME)


def emit(line, size):
    """Write the message out verbatim, then echo it for the run log."""
    destination = resolve_output_path()
    # The grader opens this file as a different user, so the file has
    # to be world-readable; without that it fails as "not readable".
    with open(destination, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    os.chmod(destination, OUTPUT_MODE)
    print(line)
    print(f"({size} characters)")


def run():
    """Validate the message, then emit it. Nothing is written unchecked."""
    size = validate_line(LINE)
    emit(LINE, size)


if __name__ == "__main__":
    run()
