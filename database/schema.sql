CREATE TABLE users (
 id UUID PRIMARY KEY,
 username TEXT,
 email TEXT,
 created_at TIMESTAMP
);

CREATE TABLE posts (
 id UUID PRIMARY KEY,
 user_id UUID,
 content TEXT,
 created_at TIMESTAMP
);

CREATE TABLE events (
 id UUID PRIMARY KEY,
 user_id UUID,
 event_type TEXT,
 created_at TIMESTAMP
);
