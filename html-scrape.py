import requests
from bs4 import BeautifulSoup

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
            listing_ids.append(link)

    return listing_ids

sample = get_listing_id('7068875')
print(sample)

# add to unit_test
# print(page.status_code)

# looks like we can get a sell history: /sell/history/7068875
# full link: https://www.discogs.com/sell/history/7068875
# may require authentication
# ^ release_id
