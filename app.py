from config import *
import json
import requests

r = requests.get('https://api.discogs.com/releases/249504', auth=(CONSUMER_KEY, CONSUMER_SECRET))

# sample response
print("Status Code: ", r.status_code)
print("Headers Content Type: ", r.headers['content-type'])
# clean json
parsed_r = json.loads(r.text)
print(json.dumps(parsed_r, indent=4))