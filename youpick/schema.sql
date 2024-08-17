DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS picks;
DROP TABLE IF EXISTS requests;

CREATE TABLE users (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE picks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL UNIQUE,
  body TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    receive_id INTEGER NOT NULL,
    status TEXT CHECK(status IN('pending', 'accepted', 'rejected')) NOT NULL DEFAULT 'pending',
    FOREIGN KEY (request_id) REFERENCES users (id),
    FOREIGN KEY (receive_id) REFERENCES users (id),
    UNIQUE (request_id, receive_id, status)
    -- I used CHATGpt to help with the UNIQUE line as I didn't want duplicate requests
    -- I also asked it how to ensure the status was one of 3 predefined values
);