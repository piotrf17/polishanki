# Parses out pages with polish definitions into a sqlite db.
# Inspired by https://github.com/tatuylonen/wikitextprocessor

import bz2
from lxml import etree
from pathlib import Path
import re
import sys

from wiktionary_db import PageDb


def extract_polish_text(text):
    languages = []
    p = re.compile(r'==Polish==\n((.|\n)*?)(==[\w-]+==\n|$)')
    m = p.search(text)
    if m is None:
        raise KeyError('no polish text found')
    return m.group(1)


def dump_failed_text(title, text):
    output_file = Path('/tmp/wiktionary/' + title)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(text)


def process_dump(dump_path, db_path):
    print(f"processing wiktionary dump at {dump_path}")
    db = PageDb(db_path)
    db.create()
    with bz2.open(dump_path, 'rb') as f:
        namespace_str = "http://www.mediawiki.org/xml/export-0.10/"
        namespaces = {None: namespace_str}
        page_nums = 0
        for _, page_element in etree.iterparse(f, tag=f"{{{namespace_str}}}page"):
            title = page_element.findtext("title", "", namespaces)
            text = page_element.findtext("revision/text", "", namespaces)

            # Skip pages that don't have any Polish definitions.
            if '==Polish==' not in text:
                continue

            try:
                polish_text = extract_polish_text(text)
                db.save_page(title, polish_text)
            except KeyError:
                print(f"ERROR: Extraction failed for '{title}'")
                dump_failed_text(title, text)

            # Clear the element to save memory.
            page_element.clear()
            # Also eliminate now-empty references from the root node to elem
            for ancestor in page_element.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]

            page_nums += 1
            if page_nums % 1000 == 0:
                print(f"  ... {page_nums} raw polish pages collected")
    db.close()


if __name__ == "__main__":
    dump_path = sys.argv[1]
    db_path = sys.argv[2]
    process_dump(dump_path, db_path)
