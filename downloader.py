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
    ("https://markets.newyorkfed.org/api/fxs/all/latest.json", "FX_Swaps_Announcements_Data.json"),
    ("https://markets.newyorkfed.org/api/ambs/all/results/summary/latest.json", "FX_Swaps_Results_Data.json"),
]

# Run the function to download and fix JSON files
download_and_fix_json(urls)
