# BASIC-INSTAGRAM-SCRAPER

This projects aims to make a basic [Instagram](https://instagram.com) scraper that will automatically get the most useful account information.
It can take in either a single usersname or a list of usernames.

## Credits

This is based on:
- [Instascrape](https://github.com/chris-greening/instascrape)

## How do I run this?

**This code is tested on python 3.8.5**

1. Install Anaconda or Miniconda or Virtualenv
2. Install required instascrape `pip install insta-scrape`
4. Run it using `python main.py` and including the arguments that you need.
    More info when you run: `python main.py -h`

## Supported Arguments

- --user  : Takes in a Single Username.
- --users : Takes in a TXT filled with one Username per line (Like the users.txt included).
- --save  : Takes in the name of a CSV file to save the data to.

## TO-DO

- Improve logging
- Let the user pick the data to be scraped
- Create a GUI