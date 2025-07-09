from flask import Flask, render_template
import sqlite3
from datetime import datetime
import threading
import time

from config import DB_NAME, SCRAPE_INTERVAL_SECONDS
from scrapers.scraper_runner import run_scraper

app = Flask(__name__)

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT company, title, link, posted_at, scraped_at FROM jobs ORDER BY scraped_at DESC')
        jobs = c.fetchall()
    return render_template('index.html', jobs=jobs)

def periodic_scraper():
    while True:
        print(f"Running scraper at {datetime.now().isoformat()}")
        run_scraper()
        time.sleep(SCRAPE_INTERVAL_SECONDS)

if __name__ == '__main__':
    threading.Thread(target=periodic_scraper, daemon=True).start()
    app.run(debug=True)