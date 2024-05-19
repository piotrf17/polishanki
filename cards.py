from flask import Flask, jsonify, g
from flask_cors import cross_origin
from google.protobuf.json_format import MessageToDict

from poldict.wiktionary_db import WiktionaryDb

app = Flask(__name__)

WIKTIONARY_DB = "data/wiktionary.sqlite"


# I'm running this locally as an app, so for expediency we store
# global variables instead of dealing with application context or sessions.
def get_wiktionary_db():
    if "wiktionary_db" not in g:
        g.wiktionary_db = WiktionaryDb(WIKTIONARY_DB)
    return g.wiktionary_db


@app.route("/")
def index():
    return "<h1>Polish Card Creator</h1>"


@app.route("/api/words/<word>")
@cross_origin(origins="http://localhost:5173")
def words(word):
    word_data, scrape_time = get_wiktionary_db().lookup(word)
    data = {"word_data": MessageToDict(word_data), "scrape_time": scrape_time}
    return jsonify(data)
