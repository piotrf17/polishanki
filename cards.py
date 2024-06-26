from flask import Flask, jsonify, g, request, current_app, make_response
from flask_cors import cross_origin
from google.protobuf import json_format

from anki.note_db import NoteDb
from anki import note_pb2
from examples.reverso_db import ReversoDb
from poldict.dictionary import Dictionary


app = Flask(__name__)

# TODO(piotrf): put these in some configuration file.
ANKI_DB = "data/anki.sqlite"
REVERSO_DB = "data/reverso.sqlite"
WORDLIST = "data/frequency_list_base_50k.txt"
NODE_FRONTEND = "http://localhost:5173"
ANKI_CSV = "../../../../anki/polish2.csv"
POLDICT_DB = "data/poldict.sqlite"


# I'm running this locally as an app, so for expediency we store
# global variables instead of dealing with application context or sessions.
def get_note_db():
    if "note_db" not in g:
        g.note_db = NoteDb(ANKI_DB)
    return g.note_db


def get_reverso_db():
    if "reverso_db" not in g:
        g.reverso_db = ReversoDb(REVERSO_DB)
    return g.reverso_db


def get_wordlist():
    if "wordlist" not in g:
        with open(WORDLIST, "r") as f:
            g.words = [line.split(";")[0] for line in f.readlines()[1:]]
    return g.words


def get_poldict():
    if "poldict" not in g:
        g.poldict = Dictionary(POLDICT_DB)
    return g.poldict


def error_response(error_text):
    current_app.logger.error(error_text)
    data = {"error": error_text}
    return make_response(jsonify(data), 400)


@app.route("/")
def index():
    return "<h1>Polish Card Creator</h1>"


@app.route("/api/words/<word>")
@cross_origin(origins=NODE_FRONTEND)
def words(word):
    try:
        word_data = get_poldict().lookup(word)
        return jsonify(json_format.MessageToDict(word_data))
    except Exception as e:
        return make_response(jsonify(error=str(e)), 500)


@app.route("/api/wordlist")
@cross_origin(origins=NODE_FRONTEND)
def wordlist():
    words = get_wordlist()
    word_to_count = get_note_db().word_to_count()
    word_to_meta = get_poldict().word_to_meta()
    result = []
    for ix, word in enumerate(words):
        word_data = {"ix": ix, "word": word, "note_count": 0}
        if word in word_to_count:
            word_data["note_count"] = word_to_count[word]
        if word in word_to_meta:
            meta = word_to_meta[word]
            word_data["has_noun"] = meta[0]
            word_data["has_verb"] = meta[1]
            word_data["has_adjective"] = meta[2]
        result.append(word_data)
    return jsonify(result)


@app.route("/api/notes_for_word/<word>")
@cross_origin(origins=NODE_FRONTEND)
def notes_for_word(word):
    protos = get_note_db().find_notes(word)
    return jsonify([json_format.MessageToDict(proto) for proto in protos])


@app.route("/api/notes", methods=("POST",))
@cross_origin(origins=NODE_FRONTEND)
def notes():
    data = request.get_json()
    current_app.logger.info(f"POST new note: {data}")
    note = json_format.ParseDict(data, note_pb2.Note())
    note_id = get_note_db().insert_note(note)
    response = {}
    response["id"] = str(note_id)
    return make_response(jsonify(response), 200)


@app.route("/api/notes/<note_id>", methods=("PUT", "DELETE"))
@cross_origin(origins=NODE_FRONTEND)
def single_note(note_id):
    if request.method == "PUT":
        data = request.get_json()
        current_app.logger.info(f"PUT note: {data}")
        if data["id"] != note_id:
            return error_response("request id does not match data")
        note = json_format.ParseDict(data, note_pb2.Note())
        get_note_db().update_note(note)
    elif request.method == "DELETE":
        get_note_db().delete_note(note_id)

    return make_response(jsonify({}), 200)


@app.route("/api/examples/<word>")
@cross_origin(origins=NODE_FRONTEND)
def examples(word):
    return jsonify(json_format.MessageToDict(get_reverso_db().examples(word)))


@app.route("/api/examples/<word>/scrape_next_page")
@cross_origin(origins=NODE_FRONTEND)
def scrape_next_page(word):
    return jsonify(json_format.MessageToDict(get_reverso_db().scrape_next_page(word)))


@app.route("/api/export_to_csv")
@cross_origin(origins=NODE_FRONTEND)
def export_to_csv():
    num_notes = get_note_db().export_to_csv(ANKI_CSV)
    current_app.logger.info(f"Wrote {num_notes} notes.")
    return jsonify(noteCount=num_notes)
