import json
from scraper_loader import load_scraper_class
from db import save_jobs

def load_companies(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def run_scraper():
    company_data = load_companies('companies.json')
    all_new_jobs = []
    for entry in company_data:
        company = entry['name']
        url = entry['link']
        try:
            ScraperClass = load_scraper_class(company)
            scraper = ScraperClass(company, url)
            jobs = scraper.fetch_jobs()
            new_jobs = save_jobs(jobs)
            all_new_jobs.extend(new_jobs)
        except NotImplementedError as e:
            print(e)
    return all_new_jobs