from scraper_base import JobLink
from datetime import datetime

class CBALink(JobLink):
    def fetch_jobs(self):
        # TODO: Implement scraping logic for CBA
        print(f"Scraping jobs from {self.url}")
        return [{
            'company': self.company,
            'title': 'Example Job Title - CBA',
            'link': self.url,
            'posted_at': datetime.now().isoformat()
        }]
