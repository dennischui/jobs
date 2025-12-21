from flask import Flask, render_template, redirect, url_for
import sqlite3
from datetime import datetime
import threading
import time
import requests

from db import DB_NAME, SCRAPE_INTERVAL_SECONDS
from scrapers.scraper_runner import run_scraper
from db import  initialise_db
import os
app = Flask(__name__)

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Fetch jobs
        c.execute('''SELECT company.name as company_name, title, location, job.link, (posted_at - datetime('now')) as current_date
              FROM job 
              LEFT JOIN company ON job.company = company.id
              WHERE expired_at IS NULL
              ORDER BY current_date ASC''')
        jobs = c.fetchall()
        
    return render_template('index.html', jobs=jobs)


@app.route('/companies')
def companies():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # Fetch companies
        c.execute('SELECT DISTINCT * FROM company ORDER BY name')
        companies = c.fetchall()
    return render_template('companies.html', companies=companies)


@app.route('/check_health')
def check_health():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT id, link FROM company')
        companies = c.fetchall()
        for company_id, link in companies:
            if link:
                try:
                    response = requests.get(link, timeout=10)
                    healthy = 1 if response.status_code == 200 else 0
                except:
                    healthy = 0
            else:
                healthy = 0
            c.execute('UPDATE company SET healthy = ? WHERE id = ?', (healthy, company_id))
        conn.commit()
    return redirect(url_for('companies'))


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