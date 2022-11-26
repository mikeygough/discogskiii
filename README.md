### About:
**discogskiii** is my final project for [Harvard CS50X](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x).

discogskiii is a flask applicaiton built using the [discogs api](https://www.discogs.com/developers). 

[discogs](https://en.wikipedia.org/wiki/Discogs) is a database of information about audio recordings, including commercial releases, promotional releases, and bootleg or off-label releases.

***i'll write a little more as it's built...***

currently supports:
- search by artist to see their vinyl discography
- search by a user's ID to see all records they have listed for sale
    i'd like to build out this table to support the albumn name, condition, price, etc.

in development:
- CSS Styling
- error handling for searches
- links to sellers
    currently supported via /user-listings which displays all items available for sale by user_id.
    i'd like to tie in some functionality that allows the user to search by artist, and see all records for sale by that artist. or click an album from the artist-search page and see how many of that album are for sale. either would require me to loop through seller information since discogs does not support marketplace lookups via their api.
- historical price information

notes:
- there is a difference between _release_ and _master_. for example, RELEASE https://www.discogs.com/release/7068875 is different from MASTER https://www.discogs.com/master/143615 though they appear to be the same record.
- my artist-search returns the master/ url. if we make a get request to that master ID, we do get a result that contains main_release id. which we can then search for specifically. in that response is the submitters and contributors? maybe these are people who have that release for sale? 
- to get copies available for sale...

1. search artist.
1.1 get master.
2. search master.
2.1 get main_release
3. scrape discogs.com/sell/release{main_release} with pd.read_html. get sellers
4. loop through sellers. loop through inventory of sellers looking for release_id. get listing
5. search marketplace for listing. return results.

issues:
- when searching through a user's inventory, it's possible for example that a user has thousands of listings. in one recent test, a user had 10,099 listings which caused my request to essentially time out. we can filter with 'status = For Sale'... and we can sort. but there aren't really good sorting fields. i can sort by listed, price, item (title of release), artist, label, catno or audio in either descending or ascending order.
- long load times. im doing the pagination before loading the page. maybe i can load the first x results,
and subsequently load more as the user scrolls?
- error if user doesn't exist when searching for a user's inventory. need to design and implement error pages
- i don't want the table headers on either /user-listings or /artist-search to show until the user makes a post request.

all data is taken from discogs.com via their api. i ❤️ you discogs.

---
### Reference:

#### Virtual Environments
Create a Python3 Virtual Environment: 
```python3 -m venv env```

Activate the Virtual Environment:
```source env/bin/activate```

Deactivate the Virtual Environment:
```deactivate```

To Remove a Virtual Environment:
```sudo em -rf venv```

---
#### Requirements.txt
Automagically create a requirements.txt file:
```pip3 freeze > requirements.txt```

Start the Flask Server:
```flask run```

Run the Flask Server in Debug Mode:
```flask --app app.py --debug run```
