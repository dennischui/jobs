from scraper_base import JobLink
from datetime import datetime

class AtlassianLink(JobLink):
    def fetch_jobs(self):
        # TODO: Implement scraping logic for Atlassian
        print(f"Scraping jobs from {self.url}")
        return [{
            'company': self.company,
            'title': 'Example Job Title - Atlassian',
            'link': self.url,
            'posted_at': datetime.now().isoformat()
        }]
