import json
import logging
from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd
import sqlite3
from datetime import datetime
import numpy as np
from bs4 import BeautifulSoup, element
import requests
from pathlib import Path
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
        self.cached_page:Path = None
        self.gen_filter_criteria = None
        self.spec_filter_criteria = None
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

    def filter_html(self,soup:BeautifulSoup) -> List[element.Tag]:
        '''
        Have 2 levels of processing (gen_listings and spec_listings) to make filtering more readeable
        This is because often specific filters are a subclass of the overall job listings, or 
        the generic filter cant capture all the job ads or filter out the correct ones. 

        If company has non standard, overwrite in child method.
        
        :param soup: Description
        :return: Description
        :rtype: List
        '''

        gen_listings = soup.select(self.gen_filter_criteria)
    
        # filter out non job listings that got caught by the selector
        # job listings have the anchor tag inside the div
        spec_listings = []
        for listing in gen_listings:
            if not listing.select(self.spec_filter_critieria):
                print("Skipping non-job listing")
                continue
            spec_listings.append(listing)
        return spec_listings

    def fetch_jobs(self, link:Path) -> pd.DataFrame:
        """Fetch jobs from Culture Amp careers page"""
        try:
            if self.cached_page:
                with open(link, "r", encoding="utf-8") as f:
                    html_content = f.read()
            else:
                # # --- UNCOMMENT FOR REAL LINK ---
                # #open the supplied link
                # response = requests.get(self.url, headers=self.headers)
                
                # response.raise_for_status()
                # html_content = response.text
                # # --- UNCOMMENT FOR REAL LINK ---
                pass
                
            soup = BeautifulSoup(html_content, 'html.parser')
            self.soup = soup
            jobs = []
            
            # Find all job listings
            job_listings = self.filter_html(soup)
            for listing in job_listings:
                job = self._parse_job_listing(listing)
                if job:
                    jobs.append(job)
            
            if len(jobs) == 0:
                #potentially error, maybe the page structure has changed.
                #TODO: figure out how to handle this
                pass #for now

            jobs_df = pd.DataFrame(columns=["Title", "Location", "Link"])
            for job in jobs:
                jobs_df = pd.concat([jobs_df, pd.DataFrame({
                    "Title": [job['title']], 
                    "Location": [job['location']], 
                    "Link": [job['link']]
                    }
                    )], ignore_index=True)

            return jobs_df
            
        except Exception as e:
            self.logger.error(f"Error fetching jobs from {self.company}: {str(e)}")
            return []
        
    
        
        
    def get_new_jobs(self, jobs_df: pd.DataFrame, db_name: str) -> List[Dict]:
        """
        Docstring for get_new_jobs
        this allows duplicates. (company, title, location) to be unique
        
        :param self: Description
        :param jobs_df: Description
        :type jobs_df: pd.DataFrame
        :param db_name: Description
        :type db_name: str
        :return: Description
        :rtype: List[Dict]
        """
        new_jobs = pd.DataFrame(columns=["Title", "Location", "Link"])
        database_jobs = pd.read_sql_query("SELECT title, location, link FROM job WHERE company = ?",
                                         sqlite3.connect(db_name), params=(self.id,))
        indexes_to_remove = []
        
        for idx, job in jobs_df.iterrows():
            if database_jobs.loc[(database_jobs['title'] == job.Title) & (database_jobs['location'] == job.Location) & (database_jobs['link'] == job.Link)].empty:
                #it's a new job
                new_jobs = pd.concat([new_jobs, job.to_frame().T], ignore_index=True)
            else:
                # store the index for popping later
                #get index of the job in database_jobs
                db_index = database_jobs.index[(database_jobs['title'] == job.Title) & (database_jobs['location'] == job.Location) & (database_jobs['link'] == job.Link)].tolist()
                assert len(db_index) == 1
                indexes_to_remove.append(int(db_index[0])) 
            # everything in new jobs is new, everything existing in result is gone (can be archived)
        expired_jobs = database_jobs.loc[list(set(database_jobs.index.tolist()).difference(indexes_to_remove))]
        print(f"New Jobs: {new_jobs}, Expired Jobs: {expired_jobs}")
        return new_jobs, expired_jobs


    def save_jobs(self, jobs_df:pd.DataFrame, DB_NAME:str):
        """Save jobs from DataFrame to database"""
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            #insert all jobs
            for idx,job in jobs_df.iterrows():
                time_now = datetime.now().isoformat()
                date_now = time_now.split("T")[0]
                c.execute('INSERT INTO job (company, location, title, link, posted_at, expired_at) VALUES (?,?, ?, ?, ?, ?)',
                        (self.id, job.Location,job.Title, job.Link, date_now, np.nan))
            conn.commit()
        return jobs_df
    
    def remove_expired_jobs(self, expired_jobs: pd.DataFrame, DB_NAME: str):
        """Remove expired jobs from database"""
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            for idx, job in expired_jobs.iterrows():
                print("removing expired jobs:", job.title)
                c.execute('UPDATE job SET expired_at = ? WHERE company = ? AND title = ? AND location = ? AND link = ?',
                          (datetime.now().isoformat(), self.id, job.title, job.location, job.link))
            conn.commit()
        return expired_jobs
    
    def add_company_to_db(self)-> int:
        """Add or update company info in the database"""
        import sqlite3
        from db import DB_NAME
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