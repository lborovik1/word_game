# Word Learning Game & English Level Test

A web app for learning vocabulary and testing your
English proficiency level (CEFR A1–C2).

## Features

### 🎮 Word Matching Game
Match words with their translations to build
your vocabulary. 7 word sets covering all CEFR
levels from A1 (1,000 words) to C2 (16,000 words).

- Text-to-speech pronunciation (🔊 buttons)
- Live stats: Level, Correct, Wrong, Accuracy
- Spaced repetition for incorrect words
- Game title shown during play

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
slots has 100 variants (2,000 total questions), so
every test attempt is unique.

**Live progress during test:**
- Correct / Wrong / Accuracy counters
- Estimated CEFR level updates in real-time
- Text-to-speech for questions and answers

**Detailed results include:**
- Your CEFR level with visual scale
- Within-level progress percentage
- Motivational feedback message
- Score breakdown by Vocabulary, Grammar, Reading

## How to Use

1. **Start the app:**
   - **Mac/Linux:** Double-click `start-game.sh`
     or run `./start-game.sh`
   - **Windows:** Double-click `start-game.bat`
   - **Windows (no Python):** Double-click
     `start-game_no_python.bat` (uses PowerShell,
     but no learning history tracking)

2. Choose "Word Matching Game" or "English Level
   Test" from the landing page

3. For the **game**: select a word set and match
   words with translations

4. For the **test**: answer 20 questions and get
   your CEFR level result

5. **Stop the server:**
   - **Mac/Linux:** Double-click `kill-game.sh`
     or run `./kill-game.sh`
   - **Windows:** Double-click `kill-game.bat`

## Requirements

- Python 3 (for the local web server)
- A modern web browser

### Installing Python on Windows

**Option A — From python.org (recommended):**

1. Go to https://www.python.org/downloads/
2. Click the big "Download Python 3.x.x" button
3. Run the downloaded installer (.exe)
4. **IMPORTANT:** Check the box at the bottom:
   ☑ "Add Python to PATH"
5. Click "Install Now"
6. When done, restart your computer
7. Double-click `start-game.bat` to play

**Option B — From Microsoft Store:**

1. Open the Microsoft Store app
2. Search for "Python 3"
3. Click "Get" or "Install"
4. Python is automatically added to PATH
5. Double-click `start-game.bat` to play

**Option C — No Python needed:**

Use `start-game_no_python.bat` instead.
This uses PowerShell to serve files, but
learning history tracking will not work.

## Game Files

Word sets generated from a frequency-ordered
English word list (top 18,000 words) translated
to Russian using Claude AI.

| File                        | Words  |
|-----------------------------|--------|
| English-Russian-200.json    | 200    |
| English-Russian-A1-1K.json  | 1,000  |
| English-Russian-A2-2K.json  | 2,000  |
| English-Russian-B1-3K.json  | 3,000  |
| English-Russian-B2-5K.json  | 5,000  |
| English-Russian-C1-9K.json  | 9,000  |
| English-Russian-C2-16K.json | 16,000 |

## Adding New Word Sets

1. Create a JSON file in `games/` folder:
   ```json
   {
       "word1": "translation1",
       "word2": "translation2"
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
word_game/
├── index.html              # Main app (single page)
├── start-game.sh           # Mac/Linux launcher
├── start-game.bat          # Windows launcher (Python)
├── start-game_no_python.bat # Windows (no Python)
├── kill-game.sh            # Mac/Linux stop server
├── kill-game.bat           # Windows stop server
├── README.md
├── website-project-description.md
├── games/
│   ├── games-registry.js
│   ├── English-Russian-200.json
│   ├── English-Russian-A1-1K.json
│   ├── English-Russian-A2-2K.json
│   ├── English-Russian-B1-3K.json
│   ├── English-Russian-B2-5K.json
│   ├── English-Russian-C1-9K.json
│   └── English-Russian-C2-16K.json
├── mytests/
│   ├── english-level-test.json
│   ├── tests-registry.js
│   ├── pool-A1-A2.json
│   ├── pool-B1.json
│   ├── pool-B2.json
│   ├── pool-C1.json
│   └── pool-C2.json
└── scripts/
    ├── README.md
    ├── build_dictionary.py
    ├── generate_games.py
    ├── generate_test_questions.py
    ├── cleanup_dictionary.py
    ├── download_dictionary.py
    └── master_dictionary.json
```

### Test Data Files

- `english-level-test.json` — test metadata,
  level descriptions, and pool file references
- `pool-A1-A2.json` — A1 & A2 questions
  (slots 1-5, 100 variants each)
- `pool-B1.json` — B1 questions
  (slots 6-9, 100 variants each)
- `pool-B2.json` — B2 questions
  (slots 10-13, 100 variants each)
- `pool-C1.json` — C1 questions
  (slots 14-17, 100 variants each)
- `pool-C2.json` — C2 questions
  (slots 18-20, 100 variants each)

## Troubleshooting

**"Failed to load" error:**
- Start using `start-game.bat` or `start-game.sh`
- Don't open `index.html` directly in browser

**Stale content after updates:**
- Press Shift+Refresh in the browser
- Registry scripts have cache-busting built in

**Python not found:**
- Install from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation
- Restart your computer after installing

**Port 8000 already in use:**
- Run `kill-game.sh` or `kill-game.bat` first
- Then start the game again
