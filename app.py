from config import *

from flask import Flask, render_template, request
import json
import requests

# turn this file into a flask application
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/artist-search", methods=["GET", "POST"])
def artist_search():
    
    # post
    if request.method == "POST":
        artist = request.form.get("artist")
        
        # pagination
        # first get number of pages:
        num_pages = json.loads(requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&key={}&secret={}".format(artist, CONSUMER_KEY, CONSUMER_SECRET)).text)['pagination']['pages']

        # initialize empty for masters
        masters = []
        uris = []
        year = []
        thumb = []

        # iterate through number of pages
        for page in range(1, num_pages + 1):
            # get data
            r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&page={}&key={}&secret={}".format(artist, page, CONSUMER_KEY, CONSUMER_SECRET)).text

            # turn string into json
            r_json = json.loads(r)

            # get album title, uri, year, and thumbnail
            for result in r_json["results"]:
                try:
                    masters.append(result["title"])
                    uris.append(result["uri"])
                    year.append(result["year"])
                    thumb.append(result["thumb"])
                except:
                    pass

        # zip data
        data = list(zip(masters, uris, year, thumb))

        # sort by year
        data = sorted(data, key = lambda x: x[2])
        base_url = 'https://www.discogs.com'

        return render_template("artist-search.html",
                               data=data, base_url=base_url)
    
    # get
    else:
        return render_template("artist-search.html")


@app.route("/user-listings", methods=["GET", "POST"])
def user_listings():

    # good test user = 'uirapuru'
    # post
    if request.method == "POST":
        user_id = request.form.get("user_id")
    
        # pagination
        # first get number of pages:
        num_pages = json.loads(requests.get("https://api.discogs.com/users/{}/inventory".format(user_id)).text)['pagination']['pages']

        # initialize empty for masters
        ids = []
        uris = []

        # iterate through number of pages
        for page in range(1, num_pages + 1):
            # get data
            r = requests.get("https://api.discogs.com/users/{}/inventory".format(user_id)).text

            # turn string into json
            r_json = json.loads(r)

            # get data
            for result in r_json["listings"]:
                try:
                    ids.append(result["id"])
                    uris.append(result["uri"])
                except:
                    pass

        # zip data
        data = list(zip(ids, uris))

        return render_template("user-listings.html",
                               data=data)

    # get
    else:
        return render_template("user-listings.html")


@app.route("/sample-request")
def sample_request():
    
    # set artist
    artist="sun ra"
    r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&key={}&secret={}".format(artist, CONSUMER_KEY, CONSUMER_SECRET)).text

    # turn string into prettyjson
    r_json = json.loads(r)
    r_json = json.dumps(r_json, indent=4)
    
    return render_template("sample-request.html",
                           artist=artist, r_json=r_json)


@app.route("/sample-marketplace")
def sample_marketplace():

    # set listing id. note this is specific per listing, and not the master id.
    listing_id = '2134134359'
    r = requests.get("https://api.discogs.com/marketplace/listings/{}".format(listing_id)).text

    # turn string into pretty json
    r_json = json.loads(r)
    r_json = json.dumps(r_json, indent=4)

    return render_template("sample-marketplace.html", 
                           listing_id=listing_id, r_json=r_json)
