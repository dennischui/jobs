import sqlite3

DB_NAME = 'jobs.db'
SCRAPE_INTERVAL_SECONDS = 3600  # 1 hour


def initialise_db(db_name):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        # Create company table
        c.execute('''
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            link TEXT NOT NULL,
            last_accessed TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            healthy INTEGER DEFAULT NULL
        );
        ''')
        
        # Create job table
        c.execute('''
        CREATE TABLE IF NOT EXISTS job (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            title TEXT,
            location TEXT,
            link TEXT,
            posted_at TIMESTAMP,
            expired_at TIMESTAMP
        );
        ''')
        
        conn.commit()
    conn.close()
    return