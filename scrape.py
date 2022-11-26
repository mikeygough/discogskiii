''' scrape discogs release page for seller ids

1. search artist.
1.1 get master.
2. search master.
2.1 get main_release
3. scrape discogs.com/sell/release{main_release} with pd.read_html. get sellers
4. loop through sellers. loop through inventory of sellers looking for release_id. get listing
5. search marketplace for listing. return results. '''

import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

from config import *
import json
import requests

# 1. search artist
artist = 'sun ra'
page = 1
r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&page={}&key={}&secret={}".format(artist, page, CONSUMER_KEY, CONSUMER_SECRET)).text
# turn string into json
r_json = json.loads(r)
# get album title, uri, year, and thumbnail
masterID = r_json['results'][0]['id']
print("masterID: ", masterID)


# 2. search master
r = requests.get("https://api.discogs.com/masters/{}".format(masterID)).text
# # turn string into json
r_json = json.loads(r)
# # 2.1 get main release
mainRelease = r_json['main_release']
print("mainRelease: ", mainRelease)


# 3. scrape discogs.com/sell/release{main_release} with pd.read_html. get sellers
df = pd.read_html('https://www.discogs.com/sell/release/{}'.format(mainRelease))
# get sellers
sellers = []
for i in range(df[1].shape[0]):
    sellers.append(df[1]['Seller'][i].split()[1])

# 4. loop through sellers. loop through inventory of sellers looking for release_id. get listing

# !! testing with one seller !! #

# pagination... uh-oh this test user has 10,000 records for sale. at 50 per page that's 200 requests just to get their collection...
# what if i implemented binary search?
# one thing i don't know is if the sort parameter only sorts my request or sorts the entire user's collection. probably the former which makes this more complicated than it first appeared...

# first get number of pages:
userId = sellers[0]
# set query params
status = 'For Sale'
sort = 'item'
pageNum = 1
resultsPerPage = 50
sortOrder = 'asc'

num_pages = json.loads(requests.get("https://api.discogs.com/users/{}/inventory".format(userId)).text)['pagination']['pages']

# initialize empty for masters
listingIds = []

## IMPLEMENT BINARY SEARCH ##
# we break out when listings[release] == mainRelease?


# get data
r = requests.get("https://api.discogs.com/users/{}/inventory?status={}&sort={}&page={}&per_page={}&sort_order={}".format(userId, status, sort, pageNum, resultsPerPage, sortOrder)).text

# turn string into json
# r_json = json.loads(r)
# print(r_json)




r = requests.get("https://api.discogs.com/marketplace/stats/release_id={}&key={}&secret={}".format(mainRelease, CONSUMER_KEY, CONSUMER_SECRET)).text

print(r)














# iterate through number of pages
# for page in range(1, num_pages + 1):
#     # get data
#     r = requests.get("https://api.discogs.com/users/{}/inventory?status={}}&sort={}".format(userId, status, artist)).text

#     # turn string into json
#     r_json = json.loads(r)
#     print(r_json)

#     # get data
#     for result in r_json["listings"]:
#         try:
#             ids.append(result["id"])
#             uris.append(result["uri"])
#         except:
#             pass

# # zip data
# data = list(zip(ids, uris))
















# explore
# print("type", type(df))
# print("len", len(df))

# df[0] is the tracklist

# print("columns", df[1].columns)
# print(df[1])

# get the seller's name
# print(df[1]['Seller'][1].split()[1])
