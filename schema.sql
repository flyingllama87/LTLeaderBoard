DROP TABLE IF EXISTS scores;

CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT CHECK (name is null or length(name) > 0),
    score INTEGER NOT NULL CHECK (typeof(score) = 'integer' and score > 0),
    difficulty TEXT CHECK (difficulty == "Easy" or difficulty == "Medium" or difficulty == "Hard")
);
