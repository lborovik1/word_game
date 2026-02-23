======================================================
In the word games and grammar games
currently the words (or grammar examples) 
are selected randomly.

We want to make algorithm more clever 
and concentrate on items that the user 
has never tried or on which he made mistakes.

For this we need to keep history of questions/answers.
All words are first marked as unknown.
As the user answers correctly or not, the mark should change.

Once a word was answered correctly last 3 times
it was asked, we mark the word as solid knowledge.
So we do not have to show it again.

Question - how can we implement this history?
Maybe keep it in a local SQLite database?
The our python server needs to be probabably a bit more
complex - to handle database storing/retrieving

Please suggest a viable solution that can work
on both Unix (Mac/Linux) and Windows computers

======================================================
Please add same type of history support 
to the grammar game

======================================================
======================================================
======================================================
