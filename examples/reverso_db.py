import sqlite3

from reverso_context_api import Client

from examples import reverso_pb2

SCHEMA = """
DROP TABLE IF EXISTS word_to_examples;

CREATE TABLE word_to_examples (
  word TEXT PRIMARY KEY,
  examples TEXT NOT NULL
);
"""


class ReversoDb(object):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def create(self):
        """Drops any existing table and creates a new one."""
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    def examples(self, word):
        """Returns a list of all Example associated with `word`."""
        result = self.conn.execute(
            "SELECT examples FROM word_to_examples WHERE word = ?", (word,)
        )
        row = result.fetchone()
        if row == None:
            return self.scrape_next_page(word)
        return reverso_pb2.Examples.FromString(row[0])

    def scrape_next_page(self, word):
        """Scrape the next page of examples for `word`, and returns all examples."""
        examples = reverso_pb2.Examples()

        # See if there are any existing examples.
        result = self.conn.execute(
            "SELECT examples FROM word_to_examples WHERE word = ?", (word,)
        )
        row = result.fetchone()
        if row != None:
            examples = reverso_pb2.Examples.FromString(row[0])

        # Scrape the next page in reverso.
        examples.latest_scraped_page += 1
        client = Client("pl", "en")
        r = client._request_translations(
            word, "pl", "en", None, examples.latest_scraped_page
        )
        for example_json in r.json()["list"]:
            example = reverso_pb2.Example()
            example.polish = client._cleanup_html_tags(example_json["s_text"])
            example.english = client._cleanup_html_tags(example_json["t_text"])
            example.source = example_json["cname"]
            examples.examples.append(example)

        # Save the examples back into the database.
        raw_examples = examples.SerializeToString()
        if examples.latest_scraped_page == 1:
            self.conn.execute(
                "INSERT INTO word_to_examples (word, examples) VALUES (?, ?)",
                (word, raw_examples),
            )
        else:
            self.conn.execute(
                "UPDATE word_to_examples SET examples = ? WHERE word = ?",
                (raw_examples, word),
            )
        self.conn.commit()

        return examples
