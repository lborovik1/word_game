in this directory "word-game" we have a simple one-page website
with a simple javascript game.

Originally this was part of a bigger website, so it has some top and bottom menu links.

Please remove all those menu.
Simplify the page as much as possible.
Remove unnecessary things.
We just need the game itself.
======================================================
Can you simplify even more?
Remove all annecessary styles and divs.

Also when I select the game from drop-down - there is an error loading the game
======================================================
I don't want to use python to start the game.
I want to just open the "index.html" file in the browser locally
======================================================
I open the index.html page by double-clicking on it in the Finder.
It opens in the browsesr. 
I can select the game - no errors. 
But When i press the button to play - nothing happens
======================================================
Currently the game code consists of two file: index.html and styles.css

Please put all styles inside the index.html, so that the whole game 
will consist of only one file index.html.

Delete (remove) the styles.css file
======================================================
Please make the game interface more compact vertically and horizontally.
The whole game should fit into the small smartphone window.
Even on computer it still should show as a vertical window.
The buttons should be always side-by-side.
They should be arranged into 2 columns and 4 rows
======================================================
Please add one more game to learn English words.
Create a file games/english100.json with 200 common
English words and their Russian translations
======================================================
why you invoke python server?
The page should work without python server. Without http server.
It should run as simple local html/javascript page
======================================================
You have created English-Russian-200.js file as a Javascript file.
Please convert it to simple JSON file - as the other two games already done.

Also please remove hardcoded info about these games from index.html

Index.html should discover which JSON files are available under the "games"
subdirectory - and show them in the drop-down

So index.html should be generic.
It should work withwhatever JSON fiels we put into the "games" folder.
======================================================
So now we have all games as Javascript files,
and we have additional "games-registry.js" file

Can we channge this to have all games as plain JSON files
without any javascript code, and keep javascript code in the "games-registry.js" file?

And keep index.html completely generic - it can only know about the "games-registry.js" file.

And make it work locally without the python http server

======================================================
please "flatten" games/ai-terms.json

Currently it is subdivided into sections.
Please remove the sections.
Put all terms into one dictionary.
So it shoudl be simple key - value structure of the whole file
Please sort by key and remove duplicates (if any)
======================================================
I want to add the "audio" buttons to the game in current directory similar how it is done in here:

/Users/levselector/Documents/GitHub/lada-pm/website/game/

======================================================
Please review the code in this repo and clean it up as necessary
Please update the README file
======================================================
I want to add an english level evaluation test.
So when the user opens index.html, he should have
option to start a game,
or to start a test.

There are standard levels of English proficiency:

CEFR = Common European Framework of Reference for Languages

CEFR defines 6 Levels:
A1 (Beginner)
A2 (Elementary)
B1 (Intermediate)
B2 (Upper Intermediate)
C1 (Advanced)
C2 (Mastery)

Level Vocabulary Size
A1  600-1,000 words
A2  1,000-2,000 words
B1  2,500-3,000 words
B2  3,000-5,000 words
C1  5,000-9,000 words
C2  8,000-16,000+ words

Ideally the test should evaluate not only the vocabulary,
but also Grammar and Reading

Please search online for test materials we can use.
Put the resources under "mytests" subdirectory.

The test should be relatively short (20 questions)
Similar to this:  https://www.ef.edu/test/english/

Please implement the test.

======================================================
You have implemented one test with 20 questions.
As we are planning to run the test periodically (once per week),
we need to add randomness into the test so that every time a student takes the test, it is different.

Please make 10 variations of each of 20 questions.
So that every time a student takes the test, 
each question will be randomly picked out of 10 possible questions.
======================================================
