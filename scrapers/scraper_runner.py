import json
import time
import logging
from scrapers.scraper_loader import load_scraper_class
from typing import List, Dict
from scrapers.culture_amp_scraper import CultureAmpScraper
from scrapers.company_scrapers import ReaGroupScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rate limiting configuration
RATE_LIMIT_DELAY = 5  # seconds between requests
MAX_RETRIES = 2
RETRY_DELAY = 30  # seconds between retries

def load_companies(filename: str) -> List[Dict]:
    with open(filename, 'r') as f:
        return json.load(f)

def run_scraper() -> List:
    company_data = load_companies('companies.json')
    all_new_jobs = []
    
    for entry in company_data:
        company = entry['name']
        url = entry['link']
        
        for attempt in range(MAX_RETRIES):
            try:
                logging.info(f"Processing {company} (attempt {attempt + 1}/{MAX_RETRIES})")
                ScraperClass = load_scraper_class(company)
                scraper = ScraperClass(company, url)
                
                # Add rate limiting delay before making request
                time.sleep(RATE_LIMIT_DELAY)
                
                jobs_df = scraper.fetch_jobs()
                new_jobs, expired_jobs = scraper.get_new_jobs(jobs_df, 'jobs.db')
                add_jobs = scraper.save_jobs(new_jobs, 'jobs.db')
                remove_jobs = scraper.remove_expired_jobs(expired_jobs, 'jobs.db')
                
                logging.info(f"Successfully scraped {len(add_jobs)} jobs from {company}")
                break  # Success - exit retry loop
                
            except NotImplementedError as e:
                logging.warning(f"Scraper not implemented for {company}: {str(e)}")
                break  # No point retrying if not implemented
                
            except Exception as e:
                logging.error(f"Error scraping {company} (attempt {attempt + 1}): {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    logging.info(f"Waiting {RETRY_DELAY} seconds before retrying...")
                    time.sleep(RETRY_DELAY)
                continue
                
    return all_new_jobs

if __name__ == "__main__":
    try:
        # new_jobs = run_scraper()
        # logging.info(f"Completed scraping with {len(new_jobs)} new jobs found")
        
        # Example usage of CanvaScraper
        scraper = CultureAmpScraper("CultureAmp", "https://www.cultureamp.com/company/careers#open-roles")
        jobs = scraper.fetch_jobs()
        for job in jobs:
            print(f"{job['title']} - {job['location']}")
            
    except Exception as e:
        logging.error(f"Fatal error in scraper runner: {str(e)}")
        raise