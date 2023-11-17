import json
import re
import requests
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fix_json_content(json_text):
    # Apply targeted fixes
    fixed_json_text = re.sub(r'": \* ', r'": null ', json_text)
    fixed_json_text = fixed_json_text.replace(", }", " }")
    fixed_json_text = fixed_json_text.replace(", ]", " ]")
    fixed_json_text = fixed_json_text.replace("'", '"')
    return fixed_json_text

def download_and_fix_json(urls):
    for url, filename in urls:
        try:
            # Download the JSON data
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for unsuccessful status codes

            if not response.text.strip():
                # Log a message if the response is empty (indicating site maintenance or data unavailability)
                logging.warning("Site Maintenance -- data temporarily unavailable.")
                continue

            # Attempt to fix the JSON content
            fixed_json_text = fix_json_content(response.text)

            # Parse the fixed content to ensure it is valid JSON
            fixed_json_data = json.loads(fixed_json_text)

            # Save the fixed JSON content to a file
            with open(filename, 'w') as outfile:
                json.dump(fixed_json_data, outfile, indent=4)
            logging.info(f"Saved fixed JSON to '{filename}'")
        except requests.HTTPError as http_err:
            logging.error(f"HTTP error occurred while downloading '{filename}': {http_err}")
        except json.JSONDecodeError as json_err:
            logging.error(f"JSON error occurred while fixing '{filename}': {json_err}")

# URLs and file names
urls = [
    ("https://markets.newyorkfed.org/api/marketshare/qtrly/latest.json", "marketshare_quarterly.json"),
    ("https://markets.newyorkfed.org/api/marketshare/ytd/latest.json", "marketshare_yearly.json")
]

# Run the function to download and fix JSON files
download_and_fix_json(urls)