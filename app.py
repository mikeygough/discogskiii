from config import *

from flask import Flask, render_template, request
import json
import requests

# turn this file into a flask application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sample-request")
def sample_request():
    artist="sun ra"

    r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&key={}&secret={}".format(artist, CONSUMER_KEY, CONSUMER_SECRET)).text
    return render_template("sample-request.html", r=r)


@app.route("/sample-request-search", methods=["GET", "POST"])
def sample_request_search():
    
    # post
    if request.method == "POST":
        artist = request.form.get("artist")
        
        r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&key={}&secret={}".format(artist, CONSUMER_KEY, CONSUMER_SECRET)).text

        # turn string into json
        r_json = json.loads(r)

        # initialize empty for masters
        masters = []
        uris = []
        year = []
        thumb = []
        
        # get album title
        for result in r_json["results"]:
            masters.append(result["title"])
            uris.append(result["uri"])
            year.append(result["year"])
            thumb.append(result["thumb"])

        data = list(zip(masters, uris, year, thumb))
        base_url = 'https://www.discogs.com'
        print(thumb[0])

        return render_template("sample-request-search.html",
                               data=data, base_url=base_url)
    
    # get
    else:
        return render_template("sample-request-search.html")

@app.route("/sample-marketplace")
def sample_marketplace():

    listing_id = '2134134359'
    # r = requests.get("https://api.discogs.com/marketplace/stats/143615").text
    r = requests.get("https://api.discogs.com/marketplace/listings/{}".format(listing_id, CONSUMER_KEY, CONSUMER_SECRET)).text

    return render_template("sample-marketplace.html", r=r)

