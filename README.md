# Word Learning Game & English Level Test

A web app for learning vocabulary and testing your
English proficiency level (CEFR A1–C2).

## Features

### 🎮 Word Matching Game
Match words with their translations to build
your vocabulary. Supports multiple word sets.

### 📝 English Level Test (CEFR)
A 20-question multiple-choice test that evaluates
your English across three categories:
- **Vocabulary** — word meanings and definitions
- **Grammar** — sentence structure and verb forms
- **Reading** — comprehension of short passages

The test covers all 6 CEFR levels:
- A1 (Beginner) — 600-1,000 words
- A2 (Elementary) — 1,000-2,000 words
- B1 (Intermediate) — 2,500-3,000 words
- B2 (Upper Intermediate) — 3,000-5,000 words
- C1 (Advanced) — 5,000-9,000 words
- C2 (Mastery) — 8,000-16,000+ words

**Randomized questions:** Each of the 20 question
slots has 10 variants (200 total questions), so
every test attempt is different — perfect for
weekly retesting.

**Detailed results include:**
- Your CEFR level with visual scale
- Within-level progress percentage (e.g. "70%
  through B1 → B2")
- Motivational feedback message
- Score breakdown by Vocabulary, Grammar, Reading

## How to Use

1. **Start the app:**
   - **Windows:** Double-click `start-game.bat`
   - **Mac/Linux:** Run `./start-game.sh`

2. Choose "Word Matching Game" or "English Level
   Test" from the landing page

3. For the **game**: select a word set and match
   words with translations

4. For the **test**: answer 20 questions and get
   your CEFR level result

## Requirements

- Python 3 (for the local web server)
- A modern web browser

### Installing Python on Windows

1. Download from https://www.python.org/downloads/
2. Check "Add Python to PATH" during installation
3. Restart your computer after installation

## Adding New Word Sets

1. Create a JSON file in `games/` folder:
   ```json
   {
       "word1": "definition1",
       "word2": "definition2"
   }
   ```

2. Edit `games/games-registry.js` and add it:
   ```javascript
   var GAMES_LIST = [
       { file: "your-file.json", name: "Name" }
   ];
   ```

3. Restart the app

## File Structure

```
word-game/
├── index.html
├── start-game.bat
├── start-game.sh
├── README.md
├── website-project-description.md
├── games/
│   ├── games-registry.js
│   └── English-Russian-200.json
└── mytests/
    ├── english-level-test.json
    ├── tests-registry.js
    ├── pool-A1-A2.json
    ├── pool-B1.json
    ├── pool-B2.json
    ├── pool-C1.json
    └── pool-C2.json
```

### Test Data Files

- `english-level-test.json` — test metadata,
  level descriptions, and pool file references
- `pool-A1-A2.json` — A1 & A2 questions
  (slots 1-5, 10 variants each)
- `pool-B1.json` — B1 questions
  (slots 6-9, 10 variants each)
- `pool-B2.json` — B2 questions
  (slots 10-13, 10 variants each)
- `pool-C1.json` — C1 questions
  (slots 14-17, 10 variants each)
- `pool-C2.json` — C2 questions
  (slots 18-20, 10 variants each)

## Troubleshooting

**"Failed to load" error:**
- Start using `start-game.bat` or `start-game.sh`
- Don't open `index.html` directly in browser

**Python not found:**
- Install from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation
- Restart your computer after installing
