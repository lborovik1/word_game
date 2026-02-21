#!/usr/bin/env python3
"""Generate 6 game JSON files from master dict."""

import json
import os
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
GAMES_DIR = os.path.join(PROJECT_DIR, "games")
MASTER_FILE = os.path.join(
    SCRIPT_DIR, "master_dictionary.json"
)
FREQ_URL = (
    "https://raw.githubusercontent.com/"
    "hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)

LEVELS = [
    ("English-Russian-A1-1K.json", 1000),
    ("English-Russian-A2-2K.json", 2000),
    ("English-Russian-B1-3K.json", 3000),
    ("English-Russian-B2-5K.json", 5000),
    ("English-Russian-C1-9K.json", 9000),
    ("English-Russian-C2-16K.json", 16000),
]

# --------------------------------------------------------------
def download_frequency_list():
    """Download English frequency word list."""
    print("Downloading frequency list...")
    req = urllib.request.Request(
        FREQ_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode("utf-8")
    return text

# --------------------------------------------------------------
def parse_words(text):
    """Parse frequency list into ordered words."""
    words = []
    seen = set()
    for line in text.strip().split("\n"):
        parts = line.strip().split()
        if not parts:
            continue
        word = parts[0].lower().strip()
        if len(word) < 2 or not word.isalpha():
            continue
        skip = ("ll", "ve", "re", "don", "didn")
        if word in skip:
            continue
        if word not in seen:
            seen.add(word)
            words.append(word)
    return words

# --------------------------------------------------------------
def load_master_dictionary():
    """Load the master EN-RU dictionary."""
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------------------------------------------
def build_ordered_dict(freq_words, master):
    """Build frequency-ordered dictionary."""
    ordered = []
    for word in freq_words:
        if word in master:
            ordered.append((word, master[word]))
    return ordered

# --------------------------------------------------------------
def generate_game_file(ordered, filename, count):
    """Generate a single game JSON file."""
    subset = ordered[:count]
    game_dict = {}
    for eng, rus in subset:
        game_dict[eng] = rus
    filepath = os.path.join(GAMES_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(
            game_dict, f,
            ensure_ascii=False, indent=2
        )
    actual = len(game_dict)
    print(f"  {filename}: {actual} words")
    return actual

# --------------------------------------------------------------
def main():
    """Main function."""
    print("Loading master dictionary...")
    master = load_master_dictionary()
    print(f"  {len(master)} translations loaded")

    print("Downloading frequency order...")
    text = download_frequency_list()
    freq_words = parse_words(text)
    print(f"  {len(freq_words)} frequency words")

    ordered = build_ordered_dict(
        freq_words, master
    )
    print(f"  {len(ordered)} matched pairs\n")

    print("Generating game files:")
    for filename, count in LEVELS:
        generate_game_file(ordered, filename, count)

    print("\nDone! All game files generated.")

# --------------------------------------------------------------
if __name__ == "__main__":
    main()
