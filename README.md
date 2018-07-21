### DESCRIPTION:
This leaderboard implementation was built for my 'LittleTiggy' game:
https://github.com/flyingllama87/LittleTiggy/

This leaderboard server is implemented in Python, Flask, JSON-RPC & stores the data in a SQLite backend.  It has a simple API of either adding a score (AddScore) or getting all scores (GetScores). Scores consist of a player's name, score and game difficulty. It has a test script (test.py) that is used to ensure the leaderboard is working correctly and that no regressions occurred during development.

### USAGE:

1) Clone the repo
2) Setup a python 3 virtual environment with Flask, Flask-JSONRPC, colorama packages.
3) Set environment variable 'FLASK_APP' to LTLeaderBoard & FLASK_ENV to either production or development depending on your requirements.
4) Run "flask init-db" and a blank DB will be created.
5) Run "flask run" to start the Leaderboard server.
6) Open a new terminal with the same virtual environment.  Optionally modify the API endpoing in test.py (default localhost should be fine for testing) and run the 'test.py' script to ensure the LeaderBoard is working correctly.

### WHAT I LEARNED:

I learned a lot about all the above technologies in building this.  I also dipped my toes in 'Test Driven Development' by writing the tests before implementing the functionality.  On the surface this seemed easy but I often found I had made mistake in the test script or the tests were not comprehensive enough.  This isn't an issue with TDD but an issue with my approach.  If you are going to approach a project with a TDD methodology, you really have to think about the tests & all the functionality you desire.  

An example of tests I didn't think of was with the AddScore method.  My initial tests would add a result with valid inputs and ensure the result was returned via GetScores.  I also added tests for ensuring the server & DB would reject invalid inputs.  However,  I didn't think of instances where the player would submit lower scores or higher scores than their previously attained scores.  In this scenario the Leaderboard should either reject their submission or update the previous score respectively.

### IMPROVEMENTS:
- Adding HTTPS.
- Adding a HTML rendering of the leaderboard.  This way you don't have to use a JSON-RPC client to see the results.
