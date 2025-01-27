-- Drop existing tables if they exist
DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS statistics;

-- Website-wide settings
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    blog_title TEXT NOT NULL,
    share_fb TEXT,       -- Share link for Facebook
    share_whatsapp TEXT, -- Share link for WhatsApp
    share_discord TEXT,  -- Share link for Discord
    setup_flag INTEGER DEFAULT 0, -- 0 = Not setup, 1 = Setup complete
    secret_key TEXT NOT NULL --
);

-- Users table (for authentication)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,  -- Email added for authentication & notifications
    password TEXT NOT NULL
);

-- Posts table (storing blog content)
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(LENGTH(title) <= 80), -- Title limited to 80 characters
    content TEXT NOT NULL,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    views INTEGER DEFAULT 0,
    url TEXT UNIQUE NOT NULL,
    likes INTEGER DEFAULT 0 -- Number of likes for a post
);

-- Comments table (linked to posts)
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved INTEGER DEFAULT 1, -- 1 = Approved, 0 = Pending
    FOREIGN KEY (post_id) REFERENCES posts (id) ON DELETE CASCADE
);

-- Statistics table (aggregated data)
CREATE TABLE IF NOT EXISTS statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_views INTEGER DEFAULT 0,
    blog_age_days INTEGER DEFAULT 0 -- Number of days the blog has existed
);
