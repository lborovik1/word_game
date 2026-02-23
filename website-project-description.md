# Website Project Description

## Overview

A single-page web application for learning
vocabulary, testing English proficiency, and
practicing grammar.
Built with vanilla HTML, CSS, and JavaScript.
No frameworks or build tools required.

## Features

### 1. Landing Page
- Clean card-based interface
- Three options: Word Matching Game,
  English Level Test, or Grammar Practice
- Responsive design for mobile and desktop

### 2. Word Matching Game
- Match words with their translations
- Multiple word sets via JSON files
- 7 game files covering all CEFR levels:
  - English Russian 200 (starter set)
  - A1: 1,000 most frequent words
  - A2: 2,000 most frequent words
  - B1: 3,000 most frequent words
  - B2: 5,000 most frequent words
  - C1: 9,000 most frequent words
  - C2: 16,000 most frequent words
- Text-to-speech audio for pronunciation
- Progress tracking (level, correct, wrong,
  accuracy)
- **Smart word selection** using SQLite history:
  prioritizes unknown and incorrectly-answered
  words over mastered ones

### 3. English Level Test (CEFR)
- 20 multiple-choice questions
- Covers Vocabulary, Grammar, and Reading
- Questions span all 6 CEFR levels:
  A1 (Beginner) through C2 (Mastery)
- Instant feedback on each answer
- Results page with:
  - Overall CEFR level determination
  - Visual CEFR scale indicator
  - Score breakdown by category
  - Level description and vocabulary range

### 4. Grammar Practice
- Multiple-choice grammar exercises
- 3 difficulty levels:
  - A1–A2: Basic grammar (articles, to be,
    simple present/past, pronouns,
    prepositions, comparatives)
  - B1–B2: Intermediate grammar (conditionals,
    present perfect, passive voice, relative
    clauses, reported speech, modals)
  - C1–C2: Advanced grammar (inversion, mixed
    conditionals, subjunctive, cleft sentences,
    advanced passive, formal structures)
- 30 questions per level
- **Smart question ordering** using SQLite
  history: shows learning/unknown questions
  first, mastered questions last
- Instant feedback (correct/wrong)
- Score tracking with accuracy percentage
- Results page with:
  - Overall score percentage
  - Motivational message
  - Per-topic score breakdown bars
- Options to retry, pick another level,
  or return home

### 5. Learning History & Smart Selection
- SQLite database tracks all answer attempts
- Each word/question has a status:
  - **unknown**: never attempted
  - **learning**: attempted but not yet mastered
  - **solid**: answered correctly 3 times in a
    row (mastered)
- Word games prioritize unknown and learning
  words; solid words are shown only when
  nothing else remains
- Grammar games order questions with learning
  and unknown items first
- History persists across sessions in a local
  `word_game.db` file
- API endpoints for history management:
  - `GET /api/history` — get item statuses
  - `POST /api/history` — record an attempt
  - `GET /api/history/next-batch` — smart
    selection of next items
  - `GET /api/history/stats` — summary stats
  - `POST /api/history/reset` — reset history

## File Structure

```
word_game/
├── index.html
├── server.py               # Python server with
│                            # SQLite history API
├── word_game.db             # SQLite database
│                            # (auto-created)
├── start-game.bat           # Windows launcher
├── start-game.sh            # Mac/Linux launcher
├── kill-game.bat            # Windows kill script
├── kill-game.sh             # Mac/Linux kill script
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
├── grammar_games/
│   ├── grammar-registry.js
│   ├── grammar-A1-A2.json
│   ├── grammar-B1-B2.json
│   └── grammar-C1-C2.json
├── mytests/
│   ├── tests-registry.js
│   ├── english-level-test.json
│   ├── pool-A1-A2.json
│   ├── pool-B1.json
│   ├── pool-B2.json
│   ├── pool-C1.json
│   └── pool-C2.json
└── scripts/
    ├── build_dictionary.py
    ├── generate_games.py
    ├── download_dictionary.py
    ├── cleanup_dictionary.py
    ├── generate_test_questions.py
    └── master_dictionary.json
```

## Server Architecture

The application uses a custom Python HTTP
server (`server.py`) that:

1. **Serves static files** — HTML, CSS, JS,
   JSON files just like `python -m http.server`
2. **Provides REST API** — endpoints for
   recording and retrieving learning history
3. **Uses SQLite** — built-in Python module,
   no external dependencies needed
4. **Cross-platform** — works on Mac, Linux,
   and Windows with Python 3

### Database Schema

```sql
-- Each answer attempt is recorded
CREATE TABLE attempts (
    id        INTEGER PRIMARY KEY,
    game_type TEXT,    -- 'word' or 'grammar'
    game_file TEXT,    -- e.g. 'English-Russian-200.json'
    item_id   TEXT,    -- word key or question id
    correct   INTEGER, -- 1=correct, 0=wrong
    timestamp TEXT     -- ISO datetime
);

-- Computed status per item
CREATE TABLE item_status (
    game_type     TEXT,
    game_file     TEXT,
    item_id       TEXT,
    status        TEXT,    -- unknown/learning/solid
    last_3        TEXT,    -- JSON array of last 3
    total_correct INTEGER,
    total_wrong   INTEGER,
    last_seen     TEXT,
    PRIMARY KEY (game_type, game_file, item_id)
);
```

### Smart Selection Algorithm

For word games, the server selects 4 words
per round with this priority:
1. At least 1 "learning" word (if available)
2. Fill remaining with "unknown" words
3. If not enough, add more "learning" words
4. Only use "solid" words as last resort

For grammar games, questions are sorted:
1. "learning" questions first (shuffled)
2. "unknown" questions next (shuffled)
3. "solid" questions last (shuffled)

## Game Files

Word sets are generated from a frequency-
ordered English word list (top 18,000 words)
translated to Russian using Claude AI.

Each level file is cumulative (includes all
words from lower levels):

| File                        | Words  |
|-----------------------------|--------|
| English-Russian-200.json    | 200    |
| English-Russian-A1-1K.json  | 1,000  |
| English-Russian-A2-2K.json  | 2,000  |
| English-Russian-B1-3K.json  | 3,000  |
| English-Russian-B2-5K.json  | 5,000  |
| English-Russian-C1-9K.json  | 9,000  |
| English-Russian-C2-16K.json | 16,000 |

## Grammar Game Files

Grammar questions organized by CEFR level
pairs with multiple-choice format:

| File                  | Questions | Levels |
|-----------------------|-----------|--------|
| grammar-A1-A2.json    | 30        | A1, A2 |
| grammar-B1-B2.json    | 30        | B1, B2 |
| grammar-C1-C2.json    | 30        | C1, C2 |

## Scripts

- `build_dictionary.py` - Downloads English
  frequency list and translates to Russian
  using Claude API. Saves master dictionary.
  Supports resume (skips existing words).
- `generate_games.py` - Reads master dictionary
  and generates 6 level-based JSON game files.
- `download_dictionary.py` - Alternative
  dictionary builder (unused).
- `cleanup_dictionary.py` - Cleans up
  dictionary entries.
- `generate_test_questions.py` - Generates
  test question pools.

## CEFR Levels Reference

| Level | Name              | Vocabulary    |
|-------|-------------------|---------------|
| A1    | Beginner          | 600-1,000     |
| A2    | Elementary        | 1,000-2,000   |
| B1    | Intermediate      | 2,500-3,000   |
| B2    | Upper Intermediate| 3,000-5,000   |
| C1    | Advanced          | 5,000-9,000   |
| C2    | Mastery           | 8,000-16,000+ |

## Technical Details

- Pure HTML/CSS/JavaScript (no frameworks)
- Custom Python HTTP server with SQLite API
- Google Fonts: DM Serif Display, Source Sans 3
- Web Speech API for text-to-speech
- JSON-based data files for games, tests,
  and grammar exercises
- Registry JS files for discoverability
- Cache-busting on registry script loads
- Launcher scripts auto-cd to project dir
  (works from Finder/Explorer double-click)
- Zero external Python dependencies
  (uses only stdlib: http.server, sqlite3,
  json, urllib)
