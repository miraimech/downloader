# json_fix

Are you trying to get JSON from an API and the JSON is incorrectly formatted? This will download the JSON in correct format!

1. Copy/paste the URL for the API in main.py:
urls = [
    ("https://your.api/here/1.json", "API 1"),
    ("https://your.api/here/2.json", "API 2")
]
2. Activate environment in terminal: json_fix % source env_temp/bin/activate
3. Download dependencies in terminal: json_fix % pip install -r requirements.txt
4. Run in terminal: json_fix % python3 main.py
   
.JSON files are now properly formatted!
