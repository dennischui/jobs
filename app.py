from flask import Flask, render_template
import sqlite3
from datetime import datetime
import threading
import time

from config import DB_NAME, SCRAPE_INTERVAL_SECONDS
from scrapers.scraper_runner import run_scraper
from scrapers.db import initialise_db
import os
app = Flask(__name__)

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Fetch jobs
        c.execute('SELECT company, title, location, link, scraped_at FROM job ORDER BY scraped_at DESC')
        jobs = c.fetchall()
        
        # Fetch companies
        c.execute('SELECT DISTINCT * FROM company ORDER BY name')
        companies = c.fetchall()
        
    return render_template('index.html', jobs=jobs, companies=companies)

def periodic_scraper():
    if not os.path.exists(DB_NAME):
        initialise_db(DB_NAME) 

    while True:
        print(f"Running scraper at {datetime.now().isoformat()}")
        run_scraper()
        time.sleep(SCRAPE_INTERVAL_SECONDS)

if __name__ == '__main__':
    threading.Thread(target=periodic_scraper, daemon=True).start()
    app.run(debug=True)