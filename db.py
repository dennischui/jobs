import sqlite3
from datetime import datetime
from config import DB_NAME

def save_jobs(jobs):
    new_jobs = []
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        for job in jobs:
            c.execute('SELECT * FROM jobs WHERE company = ? AND title = ? AND link = ?',
                      (job['company'], job['title'], job['link']))
            if not c.fetchone():
                job['scraped_at'] = datetime.now().isoformat()
                c.execute('INSERT INTO jobs (company, title, link, posted_at, scraped_at) VALUES (?, ?, ?, ?, ?)',
                          (job['company'], job['title'], job['link'], job['posted_at'], job['scraped_at']))
                new_jobs.append(job)
        conn.commit()
    return new_jobs