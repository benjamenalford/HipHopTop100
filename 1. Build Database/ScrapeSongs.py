# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import pymongo

# setup the database
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.HipHop100

collection = db.albums
collection.drop()
# set up a quick helper function


def getLatLong(url):
    response = requests.get("https://en.wikipedia.org/" + url)
    soup = BeautifulSoup(response.text, 'html.parser')
    latitude = soup.find_all('span', class_="latitude")
    longitude = soup.find_all('span', class_="longitude")
    coordinates = []
    try:
        if latitude.__len__() > 0 and longitude.__len__() > 0:
            coordinates.append(
                round(convertCoordinate(latitude[0].text[:-1]), 2))
            coordinates.append(
                round(convertCoordinate(longitude[0].text[:-1]), 2))
    except Exception as e:
        print(e)

    return coordinates


def convertCoordinate(coordinate):
    # To calculate decimal degrees, we use the DMS to decimal degree formula below:
    # Decimal Degrees = degrees + (minutes/60) + (seconds/3600)
    # DD = d + (min/60) + (sec/3600)
    degrees = coordinate.split(unicode("°", "utf-8"))
    minutes = coordinate.split(
        unicode("°", "utf-8"))[1].split(unicode("′", "utf-8"))
    seconds = coordinate.split(
        unicode("°", "utf-8"))[1].split(unicode("′", "utf-8"))

    degrees = degrees[0] if degrees[0] else 0
    minutes = minutes[0] if minutes[0] else 0

   # if seconds[1] and seconds[1][:-1] < .01:
    seconds = 0
   # else:
    #    seconds = seconds[1][:-1]

    newCoordinate = float(0)
    try:
        newCoordinate = float(degrees) + (float(minutes) /
                                          60) + (float(seconds) / 3600)
    except Exception as e:
        print(e)

    return newCoordinate


# grab the article
url = 'https://hiphopgoldenage.com/list/100-essential-hip-hop-albums/'
baseurl = 'https://en.wikipedia.org/wiki/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

results = soup.find_all('div', class_="list-item")

for result in results:
    artist = ""
    album = ""
    year = ""
    if result.h3:
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
            except Exception as e:
                print(e)

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
        bioResults = soup.find_all('div', class_="birthplace")

        # if the initial wiki page doesn't work try the alternate(s)
        if results.__len__() < 1 and bioResults.__len__() < 1:
            wikiUrl = baseurl + artist + "_(band)"
            response = requests.get(wikiUrl)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('table', class_="infobox vcard plainlist")
            bioResults = soup.find_all('div', class_="birthplace")

        if results.__len__() < 1 and bioResults.__len__() < 1:
            wikiUrl = baseurl + artist + "_(rapper)"
            response = requests.get(wikiUrl)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('table', class_="infobox vcard plainlist")
            bioResults = soup.find_all('div', class_="birthplace")

        albumInfo["wikiUrl"] = wikiUrl

        if bioResults.__len__() > 0:
            albumInfo["coordinates"] = getLatLong(bioResults[0].a["href"])
        else:
            for result in results:
                i = result.find_all('tr')
                for row in i:
                    try:
                        if row.th and (row.th.text == "Origin" or row.th.text == "Born"):
                            locations = row.td.text.split(',')
                            for location in locations:
                                if (location.strip() == "US" or location.strip() == "United States" or location.strip() == "U.S."):
                                    locations.remove(location)

                            if row.td.a:
                                coordinates = getLatLong(row.td.a["href"])
                            else:
                                coordinates = []
                            albumInfo["coordinates"] = coordinates
                            albumInfo["origin"] = locations
                    except Exception as e:
                        print(e)

        # insert to db
        collection.insert(albumInfo)
