"""Dictionary of polish words parsed and scraped from wiktionary.

Combines a sqlite database of word info parsed form a wiktionary dump,
with a wiktionary scraper to fill in inflected forms.
"""

import sqlite3

from poldict import dictionary_pb2

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

    def word_to_meta(self):
        result = self.conn.execute(
            "SELECT word, has_noun, has_verb, has_adjective FROM words"
        )
        return {row[0]: row[1:] for row in result}
