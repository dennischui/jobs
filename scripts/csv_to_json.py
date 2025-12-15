import csv
import json
from typing import List, Dict

def convert_csv_to_json(csv_path: str, json_path: str) -> None:
    """Convert CSV file to JSON format with company name and careers website link."""
    companies = []
    
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Only include companies with career website links
            if row['Company careers website']:
                company = {
                    'name': row['Company name'].strip(),
                    'link': row['Company careers website'].strip(),
                    'tier': row['reddit ranking'].strip() if row['reddit ranking'] else 'Unranked',
                    'industry': row['industry'].strip() if row['industry'] else 'Unknown'
                }
                companies.append(company)
    
    # Sort companies by name
    companies.sort(key=lambda x: x['name'])
    
    # Write to JSON file with pretty formatting
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(companies, jsonfile, indent=2)

if __name__ == "__main__":
    csv_path = r"x:\Users\Cliff\Downloads\Company list - Sheet1(1).csv"
    json_path = r"x:\Users\Cliff\Documents\VSCode\Jobs\companies.json"
    convert_csv_to_json(csv_path, json_path)
    print("Successfully created companies.json")