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

    r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&key={}&secret={}".format(artist, CONSUMER_KEY, CONSUMER_SECRET)).text
    return render_template("sample-request.html", r=r)


@app.route("/sample-request-search", methods=["GET", "POST"])
def sample_request_search():
    
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

        return render_template("sample-request-search.html",
                               data=data, base_url=base_url)
    
    # get
    else:
        return render_template("sample-request-search.html")


@app.route("/sample-marketplace")
def sample_marketplace():

    # note that listing id is specific to a listing.
    # it is NOT a release id.
    # TESTING
    listing_id = '2047141883'
    listing_id = '193145788'
    r = requests.get("https://api.discogs.com/marketplace/listings/{}&key={}&secret={}".format(listing_id, CONSUMER_KEY, CONSUMER_SECRET)).text

    return render_template("sample-marketplace.html", r=r)


@app.route("/sample-release-stats")
def sample_release_stats():

    release_id = '1067119'
    r = requests.get("https://api.discogs.com/marketplace/stats/{}&key={}&secret={}".format(release_id, CONSUMER_KEY, CONSUMER_SECRET)).text

    return render_template("sample-release-stats.html", r=r)


@app.route("/user-listings")
def user_listings():

    user = 'uirapuru'
    # pagination
    # first get number of pages:
    num_pages = json.loads(requests.get("https://api.discogs.com/users/{}/inventory".format(user)).text)['pagination']['pages']

    print(num_pages)
    # initialize empty for masters
    ids = []
    uris = []

    # iterate through number of pages
    for page in range(1, num_pages + 1):
        # get data
        r = requests.get("https://api.discogs.com/users/{}/inventory".format(user)).text

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

    return render_template("sample-user-listings.html",
                           data=data)

    print(r)

    
    return render_template("sample-user-listings.html")
