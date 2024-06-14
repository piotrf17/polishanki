"""Database of polish words scraped from wiktionary.

Combines a sqlite database to cache scrapes, with a wiktionary
scraper and parser.
"""

import sqlite3
import sys
import time
import zlib

from poldict import wiktionary_scraper


SCHEMA = """
DROP TABLE IF EXISTS pages;

CREATE TABLE pages (
  word TEXT NOT NULL,
  page BLOB NOT NULL,
  scrape_time DOUBLE NOT NULL
);
"""


class WiktionaryDb:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def create(self):
        """Drops any existing table and creates a new one."""
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    def lookup(self, word, force_rescrape=False):
        """Looks up word on wiktionary and parses out inflections.

        Args:
          word: the word to lookup
          force_rescrape: if true, forces a rescrape even if the word is
              available in the sqlite db.

        Returns:
          A tuple containing dictionary_pb2.Word and the time the page
          was scraped, or None if the word cannot be found.
        """
        if not force_rescrape:
            row = self.conn.execute(
                "SELECT page, scrape_time FROM pages WHERE word=?", (word,)
            ).fetchone()

            if row is not None:
                compressed_page = row[0]
                scrape_time = row[1]
                page = zlib.decompress(compressed_page).decode()
                proto = wiktionary_scraper.get_forms_from_html(word, page)
                return proto, scrape_time

        # Scrape HTML from wiktionary.
        page = wiktionary_scraper.get_html(word)
        compressed_page = zlib.compress(page)
        scrape_time = time.time()

        # Save in the sqlite DB.
        self.conn.execute(
            "INSERT INTO pages (word, page, scrape_time) VALUES (?, ?, ?)",
            (word, compressed_page, scrape_time),
        )
        self.conn.commit()

        proto = wiktionary_scraper.get_forms_from_html(word, page)
        return proto, scrape_time
