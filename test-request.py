from config import *
from utils import *

from flask import Flask, render_template, request
import json
import requests

# artist = 'alice coltrane'

# # pagination
# # first get number of pages:
# num_pages = json.loads(requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&key={}&secret={}".format(artist, CONSUMER_KEY, CONSUMER_SECRET)).text)['pagination']['pages']

# vinyls = []

# # iterate through number of pages
# for page in range(1, num_pages + 1):
#     # get data
#     r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&page={}&key={}&secret={}".format(artist, page, CONSUMER_KEY, CONSUMER_SECRET)).text

#     # turn string into json
#     r_json = json.loads(r)

#     # get album title, uri, year, and thumbnail
#     for result in r_json["results"]:
#         try:
#             info = {
#             'master_id': result['master_id'],
#             'title': result['title'],
#             'uri': result['uri'],
#             'year': result['year'],
#             'thumb': result['thumb'],
#             }
#             vinyls.append(info)
#         except:
#             pass

# sorted_vinyls = sorted(vinyls, key=lambda d: d['year']) 
# for vinyl in sorted_vinyls:
#     print(vinyl)
#     print()

print(get_main_release_id(master_id='32208'))


# i need master_id or main_release
# i need to store that in a button or something
