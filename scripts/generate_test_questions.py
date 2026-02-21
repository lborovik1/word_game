#!/usr/bin/env python3
"""Generate 100 variants per test slot using Claude."""

import json
import os
import anthropic

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MYTESTS_DIR = os.path.join(
    SCRIPT_DIR, "..", "mytests"
)

POOL_FILES = [
    "pool-A1-A2.json",
    "pool-B1.json",
    "pool-B2.json",
    "pool-C1.json",
    "pool-C2.json",
]

TARGET_VARIANTS = 100

# --------------------------------------------------------------
def get_client():
    """Create Anthropic client."""
    return anthropic.Anthropic()

# --------------------------------------------------------------
def load_pool(filename):
    """Load a pool JSON file."""
    path = os.path.join(MYTESTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------------------------------------------
def save_pool(filename, data):
    """Save a pool JSON file."""
    path = os.path.join(MYTESTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data, f,
            ensure_ascii=False, indent=2
        )

# --------------------------------------------------------------
def build_prompt(slot):
    """Build prompt for generating variants."""
    existing = slot["variants"]
    level = slot["level"]
    qtype = slot["type"]
    slot_num = slot["slot"]
    need = TARGET_VARIANTS - len(existing)

    samples = json.dumps(
        existing[:5], ensure_ascii=False, indent=2
    )

    return f"""Generate {need} NEW multiple-choice
questions for an English proficiency test.

Level: {level} (CEFR)
Type: {qtype}
Slot: {slot_num}

Here are some example questions for this slot
(same level, same type). Follow the EXACT same
format and difficulty:

{samples}

RULES:
- Return ONLY a JSON array of objects
- Each object has: "question", "options", "correct"
- "options" is array of exactly 4 strings
- "correct" is index 0-3 of the right answer
- Vary the correct answer position (0,1,2,3)
- All questions must be unique, no duplicates
- Match the difficulty level exactly
- For vocabulary: test different words each time
- For grammar: test the same grammar point
  but with different sentences
- For reading: create different short passages
- Do NOT repeat any of the example questions
- Return valid JSON only, no markdown fences"""

# --------------------------------------------------------------
def generate_variants(client, slot):
    """Generate new variants for a slot."""
    existing = len(slot["variants"])
    need = TARGET_VARIANTS - existing
    if need <= 0:
        return slot["variants"]

    prompt = build_prompt(slot)
    level = slot["level"]
    qtype = slot["type"]
    slot_num = slot["slot"]

    print(f"  Slot {slot_num} ({level}/{qtype}):"
          f" have {existing}, need {need}")

    all_variants = list(slot["variants"])
    remaining = need

    while remaining > 0:
        batch = min(remaining, 50)
        print(f"    Requesting {batch} variants...")

        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[{
                "role": "user",
                "content": prompt.replace(
                    f"Generate {need}",
                    f"Generate {batch}"
                )
            }]
        )

        text = msg.content[0].text.strip()
        # Remove markdown fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]

        try:
            new_qs = json.loads(text)
            valid = validate_questions(new_qs)
            all_variants.extend(valid)
            remaining -= len(valid)
            print(f"    Got {len(valid)} valid."
                  f" Total: {len(all_variants)}")
        except json.JSONDecodeError as e:
            print(f"    JSON error: {e}")
            print(f"    Retrying...")
            continue

    return all_variants[:TARGET_VARIANTS]

# --------------------------------------------------------------
def validate_questions(questions):
    """Validate question format."""
    valid = []
    for q in questions:
        if not isinstance(q, dict):
            continue
        if "question" not in q:
            continue
        if "options" not in q:
            continue
        if "correct" not in q:
            continue
        if not isinstance(q["options"], list):
            continue
        if len(q["options"]) != 4:
            continue
        if not isinstance(q["correct"], int):
            continue
        if q["correct"] < 0 or q["correct"] > 3:
            continue
        valid.append({
            "question": q["question"],
            "options": q["options"],
            "correct": q["correct"],
        })
    return valid

# --------------------------------------------------------------
def main():
    """Main function."""
    client = get_client()

    for filename in POOL_FILES:
        print(f"\nProcessing {filename}...")
        pool = load_pool(filename)

        for slot in pool["slots"]:
            slot["variants"] = generate_variants(
                client, slot
            )

        save_pool(filename, pool)
        print(f"  Saved {filename}")

    # Print summary
    print("\n=== Summary ===")
    total = 0
    for filename in POOL_FILES:
        pool = load_pool(filename)
        for s in pool["slots"]:
            n = len(s["variants"])
            total += n
            print(f"  Slot {s['slot']}"
                  f" ({s['level']}/{s['type']})"
                  f": {n} variants")
    print(f"\nTotal questions: {total}")

# --------------------------------------------------------------
if __name__ == "__main__":
    main()
