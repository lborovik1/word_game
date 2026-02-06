# Word Learning Game

A simple word matching game for learning vocabulary, terms, and translations.

## How to Play

1. **Start the game:**
   - **Windows:** Double-click `start-game.bat`
   - **Mac/Linux:** Run `./start-game.sh` in terminal

2. Select a word set from the dropdown menu
3. Click "Start Game"
4. Match words on the left with their definitions/translations on the right
5. Click a word on each side to make a match

## Requirements

- Python 3 (for the local web server)
- A modern web browser

### Installing Python on Windows

1. Download Python from https://www.python.org/downloads/
2. **Important:** Check "Add Python to PATH" during installation
3. Restart your computer after installation

## Adding New Word Sets

1. Create a new JSON file in the `games/` folder with this format:
   ```json
   {
       "word1": "definition1",
       "word2": "definition2",
       "word3": "definition3"
   }
   ```

2. Edit `games/games-registry.js` and add your new game to the list:
   ```javascript
   var GAMES_LIST = [
       { file: "ai-terms.json", name: "AI Terms" },
       { file: "your-new-file.json", name: "Your Game Name" }
   ];
   ```

3. Restart the game

## File Structure

```
word-game/
├── index.html          # Main game file
├── start-game.bat      # Windows launcher
├── start-game.sh       # Mac/Linux launcher
├── README.md           # This file
└── games/
    ├── games-registry.js       # List of available games
    ├── ai-terms.json           # AI terminology
    ├── statistics-terms.json   # Statistics terminology
    └── English-Russian-200.json # English-Russian vocabulary
```

## Troubleshooting

**"Failed to load the word set" error:**
- Make sure you started the game using `start-game.bat` (Windows) or `./start-game.sh` (Mac/Linux)
- Don't open `index.html` directly in the browser

**Python not found:**
- Install Python from https://www.python.org/downloads/
- Make sure "Add Python to PATH" was checked during installation
- Restart your computer after installing Python
