# helper functions
from config import *
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
import re


def get_master_id(artist):
    ''' REQUIRES AUTHENTICATION
        returns master_id of first result from
        discogs database artist search '''
    r = requests.get("https://api.discogs.com/database/search?artist={}&type=master&format=vinyl&page=1&key={}&secret={}".format(artist,CONSUMER_KEY, CONSUMER_SECRET)).text
    # turn string into json
    r_json = json.loads(r)
    # get master_id
    master_id = r_json['results'][0]['id']
    return master_id


def get_main_release_id(master_id):
    ''' REQUIRES AUTHENTICATION
        returns release_id of the main release'''
    r = requests.get("https://api.discogs.com/masters/{}".format(master_id)).text
    # turn string into json
    r_json = json.loads(r)
    # get release_id of main release
    main_release_id = r_json['main_release']
    return main_release_id


def get_listing_id(release_id):
    ''' returns list of listing_ids for a given release_id '''
    # set url
    url = 'https://www.discogs.com/sell/release/{}'.format(release_id)
    # request page
    page = requests.get(url, headers={'User-Agent': 'XYZ/3.0'})
    # extract html
    soup = BeautifulSoup(page.content, "html.parser")
    # extract links
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    # filter for listing_ids
    filter = "/sell/item/"
    listing_ids = []
    for link in links:
        # ? removes additional query parameters (currency)
        if filter in str(link) and '?' not in str(link):
            # regex the id
            listing_ids.append(re.findall(r'-?\d+\.?\d*', str(link)))
    # flatten the list
    listing_ids = [item for sublist in listing_ids for item in sublist]
    return listing_ids
    # add to unit_test
    # print(page.status_code)

    # looks like we can get a sell history: /sell/history/7068875
    # full link: https://www.discogs.com/sell/history/7068875
    # may require authentication
    # ^ release_id


def get_marketplace_listing(listing_id):
    ''' REQUIRES AUTHENTICATION
        return marketplace listing json '''
    r = requests.get("https://api.discogs.com/marketplace/listings/{}".format(listing_id)).text

    # turn string into pretty json
    r_json = json.loads(r)
    r_json = json.dumps(r_json, indent=4)
    return r_json


def main():
    print("GET MASTER ID")    
    master_id = get_master_id('sun ra')
    print(master_id)
    print("GET MAIN RELEASE ID")
    main_release_id = get_main_release_id(master_id)
    print(main_release_id)
    print("GET LISTING IDS")
    listing_ids = get_listing_id(main_release_id)
    print(listing_ids)
    print("GET MARKETPLACE LISTING")
    marketplace_listing = get_marketplace_listing(listing_ids[0])
    print(marketplace_listing)

if __name__ == '__main__':
    main()

