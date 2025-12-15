import json
import requests
import time
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='link_checker.log'
)

def load_companies() -> List[Dict]:
    """Load companies from JSON file"""
    with open('companies.json', 'r') as f:
        data = json.load(f)
        return data

def check_link(company: Dict) -> Dict:
    """Check if a link returns 403"""
    result = {
        'name': company['name'],
        'link': company['link'],
        'status': None,
        'error': None
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        # response = requests.get(company['link'], headers=headers, timeout=10)
        result['status'] = response.status_code
        
    except requests.exceptions.RequestException as e:
        result['error'] = str(e)
        logging.error(f"Error checking {company['name']}: {str(e)}")
    
    return result

def main():
    companies = load_companies()
    results = []
    
    for company in companies:
        logging.info(f"Checking {company['name']}...")
        result = check_link(company)
        results.append(result)
        
        # Add delay between requests
        time.sleep(2)
        
        # Print result immediately
        status = result['status'] or 'Error'
        error = f" ({result['error']})" if result['error'] else ''
        print(f"{company['name']}: {status}{error}")
    
    # Print summary of problematic links
    print("\nLinks returning 403:")
    for result in results:
        if result['status'] == 403:
            print(f"- {result['name']}: {result['link']}")
    
    # Save results to file
    with open('link_check_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Script failed: {str(e)}")
        raise