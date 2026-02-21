#!/usr/bin/env python3
"""Build EN-RU master dictionary using Claude."""

import json
import os
import time
import urllib.request
import anthropic

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
MASTER_FILE = os.path.join(
    SCRIPT_DIR, "master_dictionary.json"
)
FREQ_URL = (
    "https://raw.githubusercontent.com/"
    "hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)

# --------------------------------------------------------------
def download_frequency_list():
    """Download and parse English frequency list."""
    print("Downloading frequency list...")
    req = urllib.request.Request(
        FREQ_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req) as resp:
        text = resp.read().decode("utf-8")
    return text

# --------------------------------------------------------------
def parse_words(text, max_words=18000):
    """Extract clean words from frequency list."""
    words = []
    seen = set()
    for line in text.strip().split("\n"):
        parts = line.strip().split()
        if not parts:
            continue
        word = parts[0].lower().strip()
        if not is_valid_word(word):
            continue
        if word not in seen:
            seen.add(word)
            words.append(word)
        if len(words) >= max_words:
            break
    return words

# --------------------------------------------------------------
def is_valid_word(word):
    """Check if word is suitable for dictionary."""
    if len(word) < 2:
        return False
    if not word.isalpha():
        return False
    if word in ("ll", "ve", "re", "don", "didn"):
        return False
    return True

# --------------------------------------------------------------
def translate_batch(client, words):
    """Translate a batch of words using Claude."""
    words_str = ", ".join(words)
    prompt = (
        "Translate each English word to Russian. "
        "Return ONLY a valid JSON object with "
        "English keys and Russian values. "
        "Use the most common translation. "
        "Example: {\"hello\": \"привет\", "
        "\"cat\": \"кошка\"}\n\n"
        f"Words: {words_str}"
    )
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=8000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    response_text = msg.content[0].text.strip()
    # Extract JSON from response
    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(response_text[start:end])
    return {}

# --------------------------------------------------------------
def load_existing():
    """Load existing partial dictionary if any."""
    if os.path.exists(MASTER_FILE):
        with open(MASTER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# --------------------------------------------------------------
def save_dictionary(dictionary):
    """Save dictionary to JSON file."""
    with open(MASTER_FILE, "w", encoding="utf-8") as f:
        json.dump(
            dictionary, f,
            ensure_ascii=False, indent=2
        )

# --------------------------------------------------------------
def build_dictionary():
    """Build the full master dictionary."""
    text = download_frequency_list()
    words = parse_words(text, max_words=18000)
    print(f"Parsed {len(words)} valid words")

    existing = load_existing()
    print(f"Existing translations: {len(existing)}")

    # Filter out already translated words
    remaining = [
        w for w in words if w not in existing
    ]
    print(f"Words to translate: {len(remaining)}")

    if not remaining:
        print("All words already translated!")
        return existing, words

    client = anthropic.Anthropic()
    batch_size = 400
    dictionary = dict(existing)

    total_batches = (
        (len(remaining) + batch_size - 1)
        // batch_size
    )

    for i in range(0, len(remaining), batch_size):
        batch = remaining[i : i + batch_size]
        batch_num = i // batch_size + 1
        print(
            f"  Batch {batch_num}/{total_batches} "
            f"({len(batch)} words)..."
        )
        try:
            translations = translate_batch(
                client, batch
            )
            dictionary.update(translations)
            # Save after each batch (resume support)
            save_dictionary(dictionary)
            print(
                f"    Got {len(translations)} "
                f"translations. "
                f"Total: {len(dictionary)}"
            )
        except Exception as e:
            print(f"    Error: {e}")
            print("    Saving progress and pausing...")
            save_dictionary(dictionary)
            time.sleep(5)
        # Small delay to avoid rate limits
        time.sleep(1)

    print(f"\nFinal dictionary: {len(dictionary)} words")
    save_dictionary(dictionary)
    return dictionary, words

# --------------------------------------------------------------
def main():
    """Main function."""
    dictionary, freq_words = build_dictionary()
    print(f"Master dictionary saved to:")
    print(f"  {MASTER_FILE}")
    print(f"  Total entries: {len(dictionary)}")

# --------------------------------------------------------------
if __name__ == "__main__":
    main()
