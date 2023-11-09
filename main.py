import json
import re
import requests

def fix_json_content(json_text):
    # Apply targeted fixes
    fixed_json_text = re.sub(r'": \* ', r'": null ', json_text)
    fixed_json_text = fixed_json_text.replace(", }", " }")
    fixed_json_text = fixed_json_text.replace(", ]", " ]")
    fixed_json_text = fixed_json_text.replace("'", '"')
    return fixed_json_text

def download_and_fix_json(urls):
    for url, description in urls:
        try:
            # Download the JSON data
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            
            # Attempt to fix the JSON content
            fixed_json_text = fix_json_content(response.text)
            
            # Parse the fixed content to ensure it is valid JSON
            fixed_json_data = json.loads(fixed_json_text)
            
            # Save the fixed JSON content to a file
            output_filename = f"{description.replace(' ', '_').lower()}_fixed.json"
            with open(output_filename, 'w') as outfile:
                json.dump(fixed_json_data, outfile, indent=4)
            print(f"Saved fixed JSON for '{description}' to '{output_filename}'")
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred while downloading '{description}': {http_err}")
        except json.JSONDecodeError as json_err:
            print(f"JSON error occurred while fixing '{description}': {json_err}")

# URLs and descriptions
urls = [
    ("https://markets.newyorkfed.org/api/marketshare/qtrly/latest.json", "Market Share Quarterly"),
    ("https://markets.newyorkfed.org/api/marketshare/ytd/latest.json", "Market Share Yearly")
]

# Run the function to download and fix JSON files
download_and_fix_json(urls)