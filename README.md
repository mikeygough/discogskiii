### About:
**discogskiii** is a flask applicaiton built using the [discogs api](https://www.discogs.com/developers) that allows you to search an artist, see a list of their vinyl releases, and discover original pressings' of those releases available for sale on discogs! [discogs](https://en.wikipedia.org/wiki/Discogs) is a database of information about audio recordings, including commercial releases, promotional releases, and bootleg or off-label releases.

[check out the version 1.0 demo!](https://bit.ly/3kB3j3y)

all data is taken from discogs.com via their api. i ❤️ you discogs.

--- looking to add order book functionality.

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
