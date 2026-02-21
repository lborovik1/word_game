#!/usr/bin/env python3
"""Download English-Russian word frequency list."""

import json
import os
import re
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "scripts")
OUTPUT = os.path.join(DATA_DIR, "master_dictionary.json")

# --------------------------------------------------------------
def download_frequency_list():
    """Download English word frequency list."""
    url = (
        "https://raw.githubusercontent.com/"
        "hermitdave/FrequencyWords/master/"
        "content/2018/en/en_50k.txt"
    )
    print(f"Downloading frequency list from:\n{url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode("utf-8")
    return text

# --------------------------------------------------------------
def parse_frequency_words(text):
    """Parse frequency list into ordered words."""
    words = []
    for line in text.strip().split("\n"):
        parts = line.strip().split()
        if len(parts) >= 1:
            word = parts[0].lower().strip()
            if (
                len(word) >= 2
                and word.isalpha()
                and not word.isdigit()
            ):
                if word not in words:
                    words.append(word)
    return words

# --------------------------------------------------------------
def download_translations(words, batch_size=500):
    """Translate words using MyMemory API."""
    translations = {}
    total = len(words)
    for i in range(0, total, batch_size):
        batch = words[i : i + batch_size]
        for word in batch:
            try:
                encoded = urllib.parse.quote(word)
                url = (
                    "https://api.mymemory.translated"
                    f".net/get?q={encoded}"
                    "&langpair=en|ru"
                )
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(
                    req, timeout=10
                ) as resp:
                    data = json.loads(
                        resp.read().decode("utf-8")
                    )
                trans = data.get(
                    "responseData", {}
                ).get("translatedText", "")
                if trans and trans.lower() != word:
                    translations[word] = trans.lower()
            except Exception:
                pass
        done = min(i + batch_size, total)
        print(f"  Translated {done}/{total} words...")
    return translations

# --------------------------------------------------------------
def main():
    """Main function."""
    import urllib.parse

    print("Step 1: Downloading frequency list...")
    text = download_frequency_list()
    words = parse_frequency_words(text)
    print(f"  Found {len(words)} unique words")

    # Take top 18000 to have buffer
    words = words[:18000]
    print(f"  Using top {len(words)} words")

    print("\nStep 2: Translating to Russian...")
    print("  (This will take a while - using "
          "free API)")
    translations = download_translations(words)
    print(f"\n  Got {len(translations)} translations")

    print(f"\nSaving to {OUTPUT}")
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(
            translations, f,
            ensure_ascii=False, indent=2
        )
    print("Done!")

# --------------------------------------------------------------
if __name__ == "__main__":
    main()
