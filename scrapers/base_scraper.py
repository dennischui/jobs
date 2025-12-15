import json
import logging
from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd
import sqlite3
from datetime import datetime

class BaseScraper(ABC):
    """Base class for job scrapers"""
    
    def __init__(self, company: str, url: str):
        #connect to db and add to company table
        
        self.company = company
        self.url = url
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        self.id = self.add_company_to_db()

    def _load_config(self) -> Dict:
        """Load scraper configuration from companies.json"""
        try:
            with open('companies.json', 'r') as f:
                data = json.load(f)
                for company in data['companies']:
                    if company['name'] == self.company:
                        return company.get('scraper_config', {})
            return {}
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}

    @abstractmethod
    def fetch_jobs(self) -> List[Dict]:
        """Fetch all jobs from the career page"""
        pass

        
    def save_jobs(self, jobs_df:pd.DataFrame, DB_NAME:str):
        """Save jobs from DataFrame to database"""
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            #insert all jobs
            for idx,job in jobs_df.iterrows():
                time_now = datetime.now().isoformat()
                c.execute('INSERT INTO job (company, location, title, link, posted_at, scraped_at) VALUES (?,?, ?, ?, ?, ?)',
                        (1, job.Location,job.Title, job.Link, "NULL", time_now))
            conn.commit()
        return jobs_df
    
    def add_company_to_db(self)-> int:
        """Add or update company info in the database"""
        import sqlite3
        from config import DB_NAME
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            #check if company exists, if not insert
            c.execute('SELECT * FROM company WHERE name = ?', (self.company,))
            if not c.fetchone():
                c.execute('INSERT INTO company (name, link, last_accessed) VALUES (?, ?, CURRENT_TIMESTAMP)',
                          (self.company, self.url))
            #update last_accessed
            else:
                c.execute('UPDATE company SET link = ?, last_accessed = CURRENT_TIMESTAMP WHERE name = ?',
                          (self.url, self.company))
            conn.commit()
        #return id of company
        id = c.execute('SELECT id FROM company WHERE name = ?', (self.company,)).fetchone()[0]
        return id