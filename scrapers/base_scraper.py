import json
import logging
from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    """Base class for job scrapers"""
    
    def __init__(self, company: str, url: str):
        self.company = company
        self.url = url
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

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