from config import *
import datetime
from utils import *
from flask import Flask, render_template, request
import json
import requests

# turn this file into a flask application
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    
    # post
    if request.method == 'POST':
        artist = request.form.get('artist')

        # pagination
        # first get number of pages:
        num_pages = json.loads(requests.get('https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&key={}&secret={}'.format(artist, CONSUMER_KEY, CONSUMER_SECRET)).text)['pagination']['pages']

        vinyls = []

        # iterate through number of pages
        for page in range(1, num_pages + 1):
            # get data
            r = requests.get('https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&page={}&key={}&secret={}'.format(artist, page, CONSUMER_KEY, CONSUMER_SECRET)).text

            # turn string into json
            r_json = json.loads(r)

            # get album title, uri, year, and thumbnail
            for result in r_json['results']:
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

        return render_template('index.html',
                               sorted_vinyls=sorted_vinyls, base_url=base_url)
    
    # get
    else:
        return render_template('index.html')

@app.route('/buy', methods=['POST'])
def buy():
    
    # post
    if request.method == 'POST':
        master_id = request.form.get('master_id')

        # get main_release_id
        main_release_id = get_main_release_id(master_id)

        # get listing_ids
        listing_ids = get_listing_id(release_id=main_release_id)

        vinyls = []
        for listing_id in listing_ids:
            r = requests.get('https://api.discogs.com/marketplace/listings/{}'.format(listing_id)).text

            r_json = json.loads(r)
            
            try:
                info = {
                'uri': r_json['uri'],
                'title': r_json['release']['title'],
                'artist': r_json['release']['artist'],
                'condition': r_json['condition'],
                'comments': r_json['comments'],
                'posted': r_json['posted'],
                'price': r_json['price']['value'],
                'formatted_price': '${:,.4g}'.format(round(int(r_json['price']['value']), 2)), # is always in USD
                'in_wantlist': r_json['release']['stats']['community']['in_wantlist'],
                'in_collection': r_json['release']['stats']['community']['in_collection'],
                'thumb': r_json['release']['thumbnail']}
                vinyls.append(info)
            except:
                pass

        # if there are none for sale, return error message
        number_for_sale = len(vinyls)
        if number_for_sale < 1:
            return render_template('temp404.html')

        # get variables
        title = vinyls[0]['title']
        artist = vinyls[0]['artist']
        in_wantlist = vinyls[0]['in_wantlist']
        in_collection = vinyls[0]['in_collection']
        demand = round(in_wantlist / in_collection, 2) # should turn this into a relative measure...
        
        # format
        in_wantlist = f'{in_wantlist:,}'
        in_collection = f'{in_collection:,}'
        
        # price is this working if the prices are strings?
        highest_price = max(vinyls, key=lambda d: d['price'])['price']
        lowest_price = min(vinyls, key=lambda d: d['price'])['price']
        # format
        highest_price = '${:,.4g}'.format(round(int(highest_price), 2))
        lowest_price = '${:,.4g}'.format(round(int(lowest_price), 2))

        thumb = vinyls[0]['thumb']

        # add days since added
        for vinyl in vinyls:
            Y = int(vinyl['posted'][0:4])
            m = int(vinyl['posted'][5:7])
            d = int(vinyl['posted'][8:10])
            posted_date = datetime.date(Y, m, d)
            today = datetime.date.today()
            vinyl['formatted_posted'] = posted_date
            vinyl['days_since_listed'] = (today - posted_date).days

        # sort by condition... this doesn't work since condition isn't a scale it's words.
        sorted_vinyls = sorted(vinyls, key=lambda d: d['price']) 

        return render_template('buy.html', 
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
        return render_template('index.html', vinyls=vinyls)

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
