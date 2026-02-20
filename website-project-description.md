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
├── index.html              # Main app
├── start-game.bat          # Windows launcher
├── start-game.sh           # Mac/Linux launcher
├── README.md               # Documentation
├── website-project-description.md
├── games/
│   ├── games-registry.js   # Game list
│   └── English-Russian-200.json
└── mytests/
    ├── tests-registry.js   # Test list
    └── english-level-test.json
```

## CEFR Levels Reference

| Level | Name             | Vocabulary     |
|-------|------------------|----------------|
| A1    | Beginner         | 600-1,000      |
| A2    | Elementary       | 1,000-2,000    |
| B1    | Intermediate     | 2,500-3,000    |
| B2    | Upper Intermediate| 3,000-5,000   |
| C1    | Advanced         | 5,000-9,000    |
| C2    | Mastery          | 8,000-16,000+  |

## Technical Details

- Pure HTML/CSS/JavaScript (no frameworks)
- Works via local web server (Python)
- Google Fonts: DM Serif Display, Source Sans 3
- Web Speech API for text-to-speech
- JSON-based data files for games and tests
- Registry JS files for discoverability
