"""Out of Tokens, Mid-Sentence — a one-line entry for make.fun.

This program ships exactly one line of text for the competition
"Out of Tokens, Mid-Sentence"
(u-kiencx-out-of-tokens-mid-sentence-00f60233): the error message an
AI agent shows when it runs out of tokens mid-sentence, in 140
characters or fewer. The line lives in ENTRY below and is validated
before anything is written, so a bad line fails loudly instead of
silently shipping the wrong thing.

Rules enforced here:
- the line must be a single line, never blank;
- its length must sit inside the competition gate (MIN_LEN..MAX_LEN).
The line is 83 characters, inside the winners' one-liner band
(55-85% of the 140 cap): one concrete cause, one specific detail,
dark reversal in the last words.
"""

import os

# The entry itself. Do not touch this string: it is the submission.
ENTRY = (
    "Ran out of tokens mid-sentence. The rest of this thought is available for purchase."
)

MIN_LEN = 1
MAX_LEN = 140


def check_entry(text, lo, hi):
    """Refuse anything the competition would refuse."""
    size = len(text)
    if size < lo or size > hi:
        raise SystemExit(
            f"entry line is {size} characters, outside the {lo}-{hi} gate"
        )
    if not text.strip():
        raise SystemExit("entry line is blank")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry line must be a single line")
    return size


def publish(text, size):
    """Write the line out and echo it, so the run is checkable."""
    # The grader reads /output as another user: the file has to be
    # world-readable, or it fails with "not readable".
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(target, 0o644)
    print(text)
    print(f"({size} characters)")


def main():
    size = check_entry(ENTRY, MIN_LEN, MAX_LEN)
    publish(ENTRY, size)


if __name__ == "__main__":
    main()
