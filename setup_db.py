import sqlite3
from datetime import datetime

def setup_database():
    """Create jobs database with company and job tables"""
    
    # SQL to create company table
    create_company_table = """
    CREATE TABLE IF NOT EXISTS company (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        link TEXT NOT NULL,
        last_accessed TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        page_data TEXT
    );
    """
    
    # SQL to create job table
    create_job_table = """
    CREATE TABLE IF NOT EXISTS job (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        location TEXT,
        link TEXT NOT NULL,
        user_removed BOOLEAN DEFAULT 0,
        last_retrieved TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (company_id) REFERENCES company (id)
    );
    """
    
    try:
        # Connect to database (creates it if it doesn't exist)
        with sqlite3.connect('jobs.db') as conn:
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute(create_company_table)
            cursor.execute(create_job_table)
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_company_name ON company(name);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_company ON job(company_id);')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_retrieved ON job(last_retrieved);')
            
            conn.commit()
            
            print("Database setup completed successfully!")
            
    except sqlite3.Error as e:
        print(f"Error setting up database: {e}")
        raise

if __name__ == "__main__":
    setup_database()