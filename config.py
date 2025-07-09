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

# Company table queries
SQL_INSERT_COMPANY = """
INSERT OR REPLACE INTO company (name, link, last_accessed, page_data)
VALUES (?, ?, ?, ?);
"""

SQL_UPDATE_COMPANY_ACCESS = """
UPDATE company 
SET last_accessed = CURRENT_TIMESTAMP,
    page_data = ?
WHERE id = ?;
"""

SQL_GET_COMPANY = """
SELECT id, name, link, last_accessed, page_data 
FROM company 
WHERE name = ?;
"""

SQL_GET_ALL_COMPANIES = """
SELECT id, name, link, last_accessed 
FROM company 
ORDER BY name;
"""

# Job table queries
SQL_INSERT_JOB = """
INSERT OR REPLACE INTO job 
(company_id, title, location, link, last_retrieved)
VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP);
"""

SQL_UPDATE_JOB_STATUS = """
UPDATE job 
SET user_removed = ? 
WHERE id = ?;
"""

SQL_GET_ACTIVE_JOBS = """
SELECT 
    j.id,
    j.title,
    j.location,
    j.link,
    j.last_retrieved,
    c.name as company,
    c.id as company_id
FROM job j
JOIN company c ON j.company_id = c.id
WHERE j.user_removed = 0
ORDER BY j.last_retrieved DESC;
"""

SQL_GET_COMPANY_JOBS = """
SELECT 
    j.id,
    j.title,
    j.location,
    j.link,
    j.last_retrieved
FROM job j
WHERE j.company_id = ?
    AND j.user_removed = 0
ORDER BY j.last_retrieved DESC;
"""

SQL_CLEANUP_OLD_JOBS = """
UPDATE job
SET user_removed = 1
WHERE company_id = ?
    AND last_retrieved < ?;
"""