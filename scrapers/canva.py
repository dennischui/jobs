from scraper_base import JobLink
from datetime import datetime

class CanvaLink(JobLink):
    def fetch_jobs(self):
        # TODO: Implement scraping logic for Canva
        print(f"Scraping jobs from {self.url}")
        return [{
            'company': self.company,
            'title': 'Example Job Title - Canva',
            'link': self.url,
            'posted_at': datetime.now().isoformat()
        }]
