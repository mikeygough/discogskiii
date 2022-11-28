from config import *
from utils import *
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

        vinyls = []

        # iterate through number of pages
        for page in range(1, num_pages + 1):
            # get data
            r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&page={}&key={}&secret={}".format(artist, page, CONSUMER_KEY, CONSUMER_SECRET)).text

            # turn string into json
            r_json = json.loads(r)

            # get album title, uri, year, and thumbnail
            for result in r_json["results"]:
                try:
                    info = {
                    'master_id': result['master_id'],
                    'title': result['title'],
                    'uri': result['uri'],
                    'year': result['year'],
                    'thumb': result['thumb'],
                    }
                    vinyls.append(info)
                except:
                    pass

        # sort by year
        sorted_vinyls = sorted(vinyls, key=lambda d: d['year']) 
        base_url = 'https://www.discogs.com'

        return render_template("artist-search.html",
                               sorted_vinyls=sorted_vinyls, base_url=base_url)
    
    # get
    else:
        return render_template("artist-search.html")


@app.route("/buy", methods=["POST"])
def buy():
    # post
    if request.method == "POST":
        master_id = request.form.get("master_id")

        # get main_release_id
        main_release_id = get_main_release_id(master_id)

        # get listing_ids
        listing_ids = get_listing_id(release_id=main_release_id)

        vinyls = []
        for listing_id in listing_ids:
            r = requests.get("https://api.discogs.com/marketplace/listings/{}".format(listing_id)).text

            r_json = json.loads(r)
            
            try:
                info = {
                "title": r_json['release']['title'],
                'artist': r_json['release']['artist'],
                "uri": r_json['uri'],
                "condition": r_json['condition'],
                "price": r_json['price']['value'],
                "formatted_price": '${:.4g}'.format(round(int(r_json['price']['value']), 2)), # is always in USD
                "in_wantlist": r_json['release']['stats']['community']['in_wantlist'],
                "in_collection": r_json['release']['stats']['community']['in_collection'],
                'thumb': r_json['release']['thumbnail']}
                vinyls.append(info)
            except:
                pass

        print("Test")
        print(vinyls[0]['price'])
        print(vinyls[0]['formatted_price'])
        # if there are none for sale, return error message
        number_for_sale = len(vinyls)
        if number_for_sale < 1:
            return render_template("temp404.html")

        # get variables
        title = vinyls[0]['title']
        artist = vinyls[0]['artist']
        in_wantlist = vinyls[0]['in_wantlist']
        in_collection = vinyls[0]['in_collection']
        # should turn this into a relative measure...
        demand = round(in_wantlist / in_collection, 2)
        # format
        in_wantlist = f'{in_wantlist:,}'
        in_collection = f'{in_collection:,}'
        # price is this working if the prices are strings?
        highest_price = max(vinyls, key=lambda d: d['price'])['price']
        lowest_price = min(vinyls, key=lambda d: d['price'])['price']
        # format
        highest_price = '${:.4g}'.format(round(int(highest_price), 2))
        lowest_price = '${:.4g}'.format(round(int(lowest_price), 2))

        thumb = vinyls[0]['thumb']


        # sort by condition... this doesn't work since condition isn't a scale it's words.
        sorted_vinyls = sorted(vinyls, key=lambda d: d['price']) 

        return render_template("buy.html", 
                               sorted_vinyls=sorted_vinyls, title=title,
                               artist=artist,
                               in_wantlist=in_wantlist,
                               in_collection=in_collection,
                               highest_price=highest_price,
                               lowest_price=lowest_price,
                               number_for_sale=number_for_sale,
                               demand=demand, thumb=thumb)
    
    # get
    else: # need to add some error handling here
        return render_template("index.html", vinyls=vinyls)


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
    LISTING_IDS = ['2047141883', '2077127480', '1976205623', '2235708601', '535808221', '186636848', '1844102899', '1204954685', '2086966004', '2086958048']

    vinyls = []
    for listing_id in LISTING_IDS:
        r = requests.get("https://api.discogs.com/marketplace/listings/{}".format(listing_id)).text

        r_json = json.loads(r)

        
        try:
            info = {
            "uri": r_json['uri'],
            "condition": r_json['condition'],
            "sleeve_condition": r_json['sleeve_condition'],
            "price": round(int(r_json['price']['value']), 2),
            "currency": r_json['price']['currency'],
            "in_wantlist": r_json['release']['stats']['community']['in_wantlist'],
            "in_collection": r_json['release']['stats']['community']['in_collection']}
            vinyls.append(info)
        except:
            pass

    # turn string into pretty json
    # r_json = json.dumps(r_json, indent=4)

    return render_template("sample-marketplace.html", 
                           vinyls=vinyls)
