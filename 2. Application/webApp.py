import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from bson import Binary, Code
from bson.json_util import dumps
import pymongo


app = Flask(__name__)


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.HipHop100


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/credits')
def credits():
    return render_template("credits.html")


@app.route('/api/albumData')
def albumData():
    albums = list(db.albums.find())
    return dumps(albums)


if __name__ == "__main__":
    app.run(debug=True)
