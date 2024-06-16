"""Dictionary of polish words parsed and scraped from wiktionary.

Combines a sqlite database of word info parsed form a wiktionary dump,
with a wiktionary scraper to fill in inflected forms.
"""

import os
import sqlite3

from poldict import dictionary_pb2
from poldict import wiktionary_scraper

SCHEMA = """
DROP TABLE IF EXISTS words;

CREATE TABLE words (
  word TEXT NOT NULL,
  has_noun BOOLEAN NOT NULL,
  has_verb BOOLEAN NOT NULL,
  has_adjective BOOLEAN NOT NULL,
  proto BLOB NOT NULL
);
"""

WIKI_CACHE = "data/wiktionary_cache"


def get_html(word):
    cache_path = os.path.join(WIKI_CACHE, f"{word}.html")
    if os.path.exists(cache_path):
        return open(cache_path).read()
    html = wiktionary_scraper.get_html(word)
    open(cache_path, "wb").write(html)
    return html


class Dictionary:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def create(self):
        """Drops any existing table and creates a new one."""
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    def insert_many(self, words_and_protos):
        tuples = []
        for word, proto in words_and_protos:
            has_noun = False
            has_verb = False
            has_adjective = False
            for meaning in proto.meanings:
                if meaning.part_of_speech == dictionary_pb2.Meaning.kNoun:
                    has_noun = True
                if meaning.part_of_speech == dictionary_pb2.Meaning.kVerb:
                    has_verb = True
                if meaning.part_of_speech == dictionary_pb2.Meaning.kAdjective:
                    has_adjective = True
            tuples.append(
                (word, has_noun, has_verb, has_adjective, proto.SerializeToString())
            )
        self.conn.executemany(
            "INSERT INTO words (word, has_noun, has_verb, has_adjective, proto) VALUES (?, ?, ?, ?, ?)",
            tuples,
        )
        self.conn.commit()

    def lookup(self, word):
        # Read the word from the sqlite dictionary.
        row = self.conn.execute(
            "SELECT proto FROM words WHERE word=?", (word,)
        ).fetchone()
        if row is None:
            raise IndexError(f"word {word} not in dictionary")
        proto = dictionary_pb2.Word.FromString(row[0])

        # Now, fetch inflections from wiktionary.
        page = get_html(word)
        proto2 = wiktionary_scraper.get_forms_from_html(word, page)
        if len(proto.meanings) != len(proto2.meanings):
            raise IndexError(
                f"meaning length mismatch, base={len(proto.meanings)}, inflect={len(proto2.meanings)}"
            )
        for meaning, meaning2 in zip(proto.meanings, proto2.meanings):
            meaning.MergeFrom(meaning2)

        return proto

    def word_to_meta(self):
        result = self.conn.execute(
            "SELECT word, has_noun, has_verb, has_adjective FROM words"
        )
        return {row[0]: row[1:] for row in result}
