# Website Project Description

## Overview

A single-page web application for learning
vocabulary and testing English proficiency.
Built with vanilla HTML, CSS, and JavaScript.
No frameworks or build tools required.

## Features

### 1. Landing Page
- Clean card-based interface
- Two options: Word Matching Game or
  English Level Test
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
- Spaced repetition for incorrect words

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

## File Structure

```
word_game/
├── index.html
├── start-game.bat          # Windows launcher
├── start-game.sh           # Mac/Linux launcher
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
    └── master_dictionary.json
```

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

## Scripts

- `build_dictionary.py` - Downloads English
  frequency list and translates to Russian
  using Claude API. Saves master dictionary.
  Supports resume (skips existing words).
- `generate_games.py` - Reads master dictionary
  and generates 6 level-based JSON game files.
- `download_dictionary.py` - Alternative
  dictionary builder (unused).

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
- Works via local web server (Python)
- Google Fonts: DM Serif Display, Source Sans 3
- Web Speech API for text-to-speech
- JSON-based data files for games and tests
- Registry JS files for discoverability
- Cache-busting on registry script loads
- Launcher scripts auto-cd to project dir
  (works from Finder/Explorer double-click)
