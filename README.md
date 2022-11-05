### About:
**discogskiii** is my final project for [Harvard CS50X](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x).

discogskiii is a flask applicaiton built using the [discogs api](https://www.discogs.com/developers). 

[discogs](https://en.wikipedia.org/wiki/Discogs) is a database of information about audio recordings, including commercial releases, promotional releases, and bootleg or off-label releases.

***i'll write a little more as it's built...***

currently supports:
- search by artist to see their vinyl discography

in development:
- error handling for searches
- links to sellers
- historical price information

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
