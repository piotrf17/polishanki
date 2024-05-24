from flask import Flask, jsonify, g
from flask_cors import cross_origin
from google.protobuf.json_format import MessageToDict

from anki.note_db import NoteDb
from poldict.wiktionary_db import WiktionaryDb

app = Flask(__name__)

WIKTIONARY_DB = "data/wiktionary.sqlite"
ANKI_DB = "data/anki.sqlite"
WORDLIST = "data/frequency_list_base_50k.txt"
NODE_FRONTEND = "http://localhost:5173"


# I'm running this locally as an app, so for expediency we store
# global variables instead of dealing with application context or sessions.
def get_wiktionary_db():
    if "wiktionary_db" not in g:
        g.wiktionary_db = WiktionaryDb(WIKTIONARY_DB)
    return g.wiktionary_db


def get_note_db():
    if "note_db" not in g:
        g.note_db = NoteDb(ANKI_DB)
    return g.note_db


def get_wordlist():
    if "wordlist" not in g:
        with open(WORDLIST, "r") as f:
            g.words = [line.split(";")[0] for line in f.readlines()[1:]]
    return g.words


@app.route("/")
def index():
    return "<h1>Polish Card Creator</h1>"


@app.route("/api/words/<word>")
@cross_origin(origins=NODE_FRONTEND)
def words(word):
    word_data, scrape_time = get_wiktionary_db().lookup(word)
    data = {"word_data": MessageToDict(word_data), "scrape_time": scrape_time}
    return jsonify(data)


@app.route("/api/wordlist")
@cross_origin(origins=NODE_FRONTEND)
def wordlist():
    words = get_wordlist()
    return jsonify(words)


@app.route("/api/notes/<word>")
@cross_origin(origins=NODE_FRONTEND)
def notes(word):
    protos = get_note_db().find_notes(word)
    return jsonify([MessageToDict(proto) for proto in protos])
