import sqlite3

def init_db():
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posted_movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER UNIQUE,
            title TEXT,
            language TEXT,
            year INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def is_movie_posted(tmdb_id):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM posted_movies WHERE tmdb_id = ?', (tmdb_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_movie_posted(tmdb_id, title, language, year):
    conn = sqlite3.connect('movies.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO posted_movies (tmdb_id, title, language, year)
        VALUES (?, ?, ?, ?)
    ''', (tmdb_id, title, language, year))
    conn.commit()
    conn.close()

init_db()
