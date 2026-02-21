#!/usr/bin/env python3
"""Clean up master dictionary - remove bad words."""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_FILE = os.path.join(
    SCRIPT_DIR, "master_dictionary.json"
)

# Words to remove: not real English words,
# archaic, abbreviations, contractions, etc.
BAD_WORDS = {
    "ye", "la", "el", "de", "em", "er", "um",
    "uh", "ah", "oh", "hm", "ha", "ho", "hi",
    "ya", "yo", "na", "da", "ma", "pa",
    "le", "en", "es", "il", "un", "du",
    "si", "se", "te", "tu", "mi", "ti",
    "al", "di", "ne", "ni", "li", "lo",
    "ta", "ka", "ba", "bi", "bo", "bu",
    "fa", "fi", "fo", "fu", "ga", "gi",
    "oi", "oy", "ay", "aw", "ew",
    "mm", "huh", "hmm", "uhh", "ahh",
    "nah", "yah", "mhm", "ugh",
    "gonna", "wanna", "gotta", "kinda",
    "sorta", "coulda", "shoulda", "woulda",
    "ain", "tis", "twas",
    "ll", "ve", "re", "don", "didn",
    "doesn", "wasn", "weren", "hasn",
    "hadn", "wouldn", "couldn", "shouldn",
    "isn", "aren", "won",
}

# --------------------------------------------------------------
def load_dictionary():
    """Load master dictionary."""
    with open(MASTER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------------------------------------------
def save_dictionary(d):
    """Save master dictionary."""
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

# --------------------------------------------------------------
def is_bad_entry(eng, rus):
    """Check if a dictionary entry is bad."""
    # Word is in the bad words list
    if eng.lower() in BAD_WORDS:
        return True
    # Translation is same as English (untranslated)
    if rus.lower() == eng.lower():
        return True
    # Very short words (1 char)
    if len(eng) < 2:
        return True
    # Translation is empty
    if not rus.strip():
        return True
    # Word is not alphabetic
    if not eng.isalpha():
        return True
    return False

# --------------------------------------------------------------
def main():
    """Main function."""
    d = load_dictionary()
    original = len(d)
    print(f"Original dictionary: {original} words")

    removed = []
    cleaned = {}
    for eng, rus in d.items():
        if is_bad_entry(eng, rus):
            removed.append((eng, rus))
        else:
            cleaned[eng] = rus

    print(f"Removed: {len(removed)} bad entries")
    print(f"Cleaned dictionary: {len(cleaned)} words")

    if removed:
        print("\nSample removed entries:")
        for eng, rus in removed[:30]:
            print(f"  {eng} -> {rus}")
        if len(removed) > 30:
            print(f"  ... and {len(removed)-30} more")

    save_dictionary(cleaned)
    print(f"\nSaved cleaned dictionary.")

# --------------------------------------------------------------
if __name__ == "__main__":
    main()
