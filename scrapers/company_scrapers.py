from typing import List, Dict
import requests
from bs4 import BeautifulSoup, element
from .base_scraper import BaseScraper
import pandas as pd
from pathlib import Path

class ReaGroupScraper(BaseScraper):
    """Scraper for REA Group careers page"""

    def __init__(self, company: str, url: str):
        super().__init__(company, url)
        self.base_url = "https://www.rea-group.com"
        self.headers.update({
            'Accept': 'application/json',
            'Referer': 'https://www.rea-group.com/careers/jobs'
        })
        # add to company table in db
        self.add_company_to_db()
        self.cached_page = Path(r"./sample_pages/REA Group response text new.htm")
        self.gen_filter_criteria = '.l-job-listing__item'
        self.spec_filter_criteria = 'a'




    def _parse_job_listing(self, listing: BeautifulSoup) -> Dict:
        """Parse individual job listing to extract out
            - Job Title
            - Company Name
            - Location
            - Link
            -  
        """
        try:
            title = listing.find('div', class_='c-job__title').text.strip()
            location = ''.join([i.strip() for i in listing.select('.c-job__col')[1].children if isinstance(i,str) ])
            link = listing.find('a').get('href')
            return {
                'title': title,
                'company': self.company,
                'location': location,
                'link': link,
                'source': 'REA Group Careers'
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing job listing: {str(e)}")
            return None

class CultureAmpScraper(BaseScraper):
    """Scraper for Culture Amp careers page"""
    
    def __init__(self, company: str, url: str):
        super().__init__(company, url)
        self.base_url = "https://boards.greenhouse.io/cultureamp"
        self.headers.update({
            'Accept': 'application/json',
            'Referer': 'https://www.cultureamp.com/company/careers'
        })
        self.cached_page = Path(r"./sample_pages/Culture Amp response text copy.htm")
        self.gen_filter_criteria = 'a'
        self.spec_filter_criteria = "https://job-boards.greenhouse.io/cultureamp/jobs/" not in listing.get('href', '')
        # add to company table in db
        self.add_company_to_db()

    def _parse_job_listing(self, listing: BeautifulSoup) -> Dict:
        """Parse individual job listing"""
        try:
            title, location = listing.select('p')
            link = listing.get('href')
            return {
                'title': title.text.strip(),
                'company': self.company,
                'location': location.text.strip(),
                'link': link,
                'source': 'Culture Amp Careers'
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing job listing: {str(e)}")
            return None
