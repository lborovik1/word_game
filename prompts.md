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
when I start start-game.sh from terminal - it works.
But when i try to start it by double-clicking on the file in the finder,
it doesn't work. It ends up showing files in the directory
How to make it work?
======================================================
It worked. Please also check the start-game.bat file. Is it OK ?
======================================================
Currently we have a game file for 200 words.
Please create 6 more games for
six standard levels:
A1  1,000 words
A2  2,000 words
B1  3,000 words
B2  5,000 words
C1  9,000 words
C2  16,000+ words

Note, as the task of creating large lists may take
a lot of tokens, please handle the words using 
automatic scripts to avoid overloading the context length of the model.

Step1:
Please find on the web and download the list of most 
common 16,000 English words
and their Russian translations
This will be our master dictionary.

Step2: 
Write a python script to generate the 6 json dictionaries
in "games" directory:
   "English-Russian-A1-1K.json" with 1 thousand words
   "English-Russian-A2-2K.json" with 2 thousand words
   "English-Russian-B1-3K.json" with 3 thousand words
   "English-Russian-B2-5K.json" with 5 thousand words
   "English-Russian-C1-9K.json" with 9 thousand words
   "English-Russian-C2-16K.json" with 16 thousand words

Step3:
Register those files in games-registry.js file
Please create a game "English-Russian-A2-2K.json
containing 2 thousand words

======================================================
For tests we have 20 question slots, 10 variants per slot, 
200 total unique questions across all pools

Let's increase the number of variant for each slot to 100.

So it should be:

20 question slots, 100 variants per slot, 
2000 total unique questions across all pools
======================================================
For tests please add the "speak" buttons next to the question and answers
(similar how we have it in the game).
======================================================
For the tests please add progress indicators
similar how we have it in the games 
(number of correct and wrong answers, ...)
So that as the person does the test, he can see approximately
how he is doing
======================================================
we currently have scripts to start the game (python server)

start-game.bat
start-game.sh

Please also create scripts to stop running server

kill-game.bat
kill-game.sh

The "sh" should run on Mac and Linux.
the "bat" on Windows.

Both scripts can be invoked from terminal - or by double-clicking
on them in Finder or Windows Explorer
======================================================
Please update the README.md file

Also please add a short scripts/README.md file 
do describe the purpose and function of each script

======================================================
We have a word game and tests.
on the home page we either go into word game or into test

Please create one more option - a game to study grammar.
Please put resources for this game in subdirectory "grammar_games".
We can do it similar to how grammar is presented in "mytests".
Questions with multiple choice answers

Please implement the grammar games.
======================================================
Please add a restart button to the grammar practice instead of the "Home" button. So that we could return to the home screen - and choose a different game or test
======================================================