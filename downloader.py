import json
import re
import requests
import logging
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fix_json_content(json_text):
    # Apply targeted fixes
    fixed_json_text = re.sub(r'": \* ', r'": null ', json_text)
    fixed_json_text = fixed_json_text.replace(", }", " }")
    fixed_json_text = fixed_json_text.replace(", ]", " ]")
    fixed_json_text = fixed_json_text.replace("'", '"')
    return fixed_json_text

def is_empty_field(data):
    if isinstance(data, dict):
        return all(is_empty_field(value) for value in data.values())
    elif isinstance(data, list):
        return len(data) == 0
    return False  # Non-container fields are not considered empty

def download_and_fix_json(urls):
    for url, filename in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            if not response.text.strip():
                logging.warning("Site Maintenance -- data temporarily unavailable.")
                continue

            fixed_json_text = fix_json_content(response.text)
            new_data = json.loads(fixed_json_text)

            if is_empty_field(new_data):
                logging.warning("Not enough data!")
                continue

            if os.path.exists(filename):
                with open(filename, 'r') as existing_file:
                    existing_data = json.load(existing_file)

                if new_data == existing_data:
                    logging.info(f"No new data found for '{filename}'.")
                    continue
                else:
                    logging.debug(f"Data difference detected for {filename}")

            with open(filename, 'w') as outfile:
                json.dump(new_data, outfile, indent=4)
            logging.info(f"Saved fixed JSON to '{filename}'")
        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred while downloading '{filename}': {http_err}")
        except json.JSONDecodeError as json_err:
            logging.error(f"JSON error occurred while fixing '{filename}': {json_err}")

# URLs and file names
urls = [
    ("https://www.federalregister.gov/api/v1/public-inspection-documents/current.json", "Public_Inspection_Data.txt"),
    ("https://markets.newyorkfed.org/api/ambs/all/announcements/summary/latest.json", "AMBS_Announcements_Data.txt"),
    ("https://markets.newyorkfed.org/api/ambs/all/results/summary/latest.json", "AMBS_Results_Data.txt"),
    ("https://markets.newyorkfed.org/api/fxs/all/latest.json", "FX_Swaps_Announcements_Data.txt"),
    ("https://markets.newyorkfed.org/api/ambs/all/results/summary/latest.json", "FX_Swaps_Results_Data.txt"),
    ("https://markets.newyorkfed.org/api/marketshare/qtrly/latest.json", "Market_Share_Quarterly_Data.txt"),
    ("https://markets.newyorkfed.org/api/marketshare/ytd/latest.json", "Market_Share_Yearly_Data.txt"),
    ("https://markets.newyorkfed.org/api/rates/all/latest.json", "Rates_Data.txt"),
    ("https://markets.newyorkfed.org/api/rp/all/all/results/latest.json", "Repo_Results_Data.txt"),
    ("https://markets.newyorkfed.org/api/rp/all/all/announcements/latest.json", "Repo_Announcemens_Data.txt"),
    ("https://markets.newyorkfed.org/api/seclending/all/results/summary/latest.json", "Securities_Lending_Data.txt"),
    ("https://markets.newyorkfed.org/api/soma/asofdates/latest.json", "SOMA_Data.txt"),
    ("https://markets.newyorkfed.org/api/tsy/all/announcements/summary/latest.json", "Treasury_Securities_Announcements_Data.txt"),
    ("https://markets.newyorkfed.org/api/tsy/all/results/summary/latest.json", "Treasury_Securities_Results_Data.txt"),
    ("https://markets.newyorkfed.org/api/tsy/all/operations/summary/latest.json", "Treasury_Securities_Operations_Data.txt"),
    
]

# Run the function to download and fix JSON files
download_and_fix_json(urls)
