-- DROP TABLE IF EXISTS users;
-- DROP TABLE IF EXISTS main;
-- DROP TABLE IF EXISTS private;
-- DROP TABLE IF EXISTS requests;
-- -- Old tables below
-- DROP TABLE IF EXISTS location;
-- DROP TABLE IF EXISTS picks;


CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS main (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS private (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    response TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
    FOREIGN KEY (recipient_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    receive_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    CHECK(status IN ('pending', 'accepted', 'rejected')),
    FOREIGN KEY (request_id) REFERENCES users (id),
    FOREIGN KEY (receive_id) REFERENCES users (id),
    UNIQUE (request_id, receive_id)
    -- I used CHATGpt to help with the UNIQUE line as I didn't want duplicate requests
    -- I also asked it how to ensure the status was one of 3 predefined values
    -- SELECT requests.*, user1.username AS sender, user2.username AS receiver FROM requests JOIN users AS user1 ON request_id = user1.id JOIN users as user2 ON receive_id = user2.id; 
    -- Query to help find sender and receiver ^ chatgpt helped to come up with the query
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commenter_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (commenter_id) REFERENCES users (id),
    FOREIGN KEY (message_id) REFERENCES main (id)
);