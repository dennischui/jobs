from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper

class CultureAmpScraper(BaseScraper):
    """Scraper for Culture Amp careers page"""
    
    def __init__(self, company: str, url: str):
        super().__init__(company, url)
        self.base_url = "https://www.cultureamp.com"
        self.headers.update({
            'Accept': 'application/json',
            'Referer': 'https://www.cultureamp.com/company/careers'
        })

    def fetch_jobs(self) -> List[Dict]:
        """Fetch jobs from Culture Amp careers page"""
        try:
            # First get the careers page
            response = requests.get(self.url, headers=self.headers)
            self.response=response
            response.raise_for_status()
            
            # The actual jobs are loaded via Greenhouse API
            greenhouse_url = "https://boards.greenhouse.io/cultureamp"
            response = requests.get(greenhouse_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            self.soup = soup
            jobs = []
            
            # Find all job listings
            job_listings = soup.select('a')
            for listing in job_listings:
                #check that the listing is a job listing by checking href
                if "https://job-boards.greenhouse.io/cultureamp/jobs/" not in listing.get('href', ''):
                    continue
                job = self._parse_job_listing(listing)
                if job:
                    jobs.append(job)
                    
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error fetching jobs from {self.company}: {str(e)}")
            return []

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