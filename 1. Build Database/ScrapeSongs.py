# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import pymongo

# setup the database
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.HipHop100
collection = db.albums

# grab the
url = 'https://hiphopgoldenage.com/list/100-essential-hip-hop-albums/'
baseurl = 'https://en.wikipedia.org/wiki/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

results = soup.find_all('div', class_="list-item")

for result in results:
    artist = ""
    album = ""
    year = ""

    try:
        resultText = result.h3.text.replace(unicode("–", "utf-8"), "-")
        artistAlbum = resultText.split(" - ")
        artist = artistAlbum[0]
        album = artistAlbum[1][:-6]
        year = artistAlbum[1][-6:].replace('(', '').replace(')', '')
    except:
        try:
            artist = "various"
            album = result.h3.text[:-6]
            year = result.h3.text[-6:].replace('(', '').replace(')', '')
        except:
            2+2

    albumInfo = {
        'artist': artist.strip(),
        'albumTitle': album.strip(),
        'year': year.strip()
    }

    # get wikipedia info
    wikiUrl = baseurl + artist
    response = requests.get(wikiUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('table', class_="infobox vcard plainlist")
    for result in results:
        i = result.find_all('tr')
        for row in i:
            try:
                if row.th.text == "Origin":
                    locations = row.td.text.split(',')
                    for location in locations:
                        if (location.strip() == "US" or location.strip() == "United States" or location.strip() == "U.S."):
                            locations.remove(location)

                    albumInfo["origin"] = locations

            except:
                2 + 2

    # insert to db
    collection.insert(albumInfo)
