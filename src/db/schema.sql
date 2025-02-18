-- User
-- id: int
-- discord_name: string
-- display_name: string optional

-- SQL for creating the User table in SQLite
CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    discord_name TEXT NOT NULL,
    display_name TEXT
);

-- Attempt
-- id: int
-- user_id: int
-- date: string
-- attempt_time: string
-- score: int

-- SQL for creating the Attempt table in SQLite
CREATE TABLE Attempt (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    attempt_time TEXT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id)
);
