from flask import Flask, jsonify
from flask_cors import cross_origin

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Polish Card Creator</h1>"


@app.route("/api/words/<word>")
@cross_origin()
def words(word):
    data = {}

    data["word"] = word
    data["inflection"] = {
        "nominative": "nom",
        "genitive": "gen",
    }

    return jsonify(data)
