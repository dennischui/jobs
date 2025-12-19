import sqlite3
from datetime import datetime
from config import DB_NAME
import pandas as pd 

def initialise_db(db_name):
    with sqlite3.connect(db_name) as conn:
        c = conn.cursor()
        # Create company table
        c.execute('''
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            link TEXT,
            last_accessed TIMESTAMP
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
            scraped_at TIMESTAMP,
        );
        ''')
        
        conn.commit()
        return