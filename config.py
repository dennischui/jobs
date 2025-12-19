from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    COMPANIES_FILE: str = "companies.json"
    LOG_FILE: str = "scraper.log"
    LOG_LEVEL: str = "INFO"
    DB_CONNECTION: Optional[str] = None

DB_NAME = 'jobs.db'
SCRAPE_INTERVAL_SECONDS = 3600  # 1 hour
