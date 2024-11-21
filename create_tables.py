import sqlite3

# 5. SQLite connection
db_filename = 'imdb.db'
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# table creations
cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        person_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        born INTEGER,
        died INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS crew (
        title_id INTEGER,
        person_id INTEGER,
        category TEXT,
        job TEXT,
        character TEXT,
        PRIMARY KEY (title_id, person_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        title_id INTEGER PRIMARY KEY,
        rating NUMERIC,
        votes NUMERIC
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS titles (
        title_id INTEGER PRIMARY KEY,
        type TEXT,
        primary_title TEXT, 
        original_title TEXT,
        is_adult INT,
        premiered INT,
        ended INT,
        runtime INTEGER,
        genres TEXT
    )
""")

