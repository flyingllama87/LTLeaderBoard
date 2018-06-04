DROP TABLE IF EXISTS scores;

CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    score INTEGER NOT NULL CHECK (typeof(score) = 'integer')
);