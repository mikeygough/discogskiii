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
- error handling
- unit testing
- historical price information


notes:
- master_id is the highest class of a vinyl record and represents the music. release_id represents a physical batch of vinyl records that were pressed. for example, release https://www.discogs.com/release/7068875 is a pressing of master https://www.discogs.com/master/143615.


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
