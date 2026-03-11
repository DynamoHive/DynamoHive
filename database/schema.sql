CREATE TABLE IF NOT EXISTS users (

    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS posts (

    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    topic TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS topics (

    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    authority_score INTEGER DEFAULT 0

);

CREATE TABLE IF NOT EXISTS events (

    id SERIAL PRIMARY KEY,
    event_type TEXT,
    payload JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);
