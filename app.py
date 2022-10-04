from config import *

from flask import Flask, render_template, request
import json
import requests

# turn this file into a flask application
app = Flask(__name__)

@app.route("/")
def index():
    r = requests.get('https://api.discogs.com/releases/249504', auth=(CONSUMER_KEY, CONSUMER_SECRET))

    # sample response
    # print("Status Code: ", r.status_code)
    # print("Headers Content Type: ", r.headers['content-type'])
    # clean json
    parsed_r = json.loads(r.text)
    # print(json.dumps(parsed_r, indent=4))    
    
    return render_template("index.html", parsed_r=parsed_r)



