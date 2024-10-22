# Parses out pages with polish definitions into a sqlite db.
# Inspired by https://github.com/tatuylonen/wikitextprocessor

import bz2
import dbm
from lxml import etree
from pathlib import Path
import os
import re
import sys

from absl import app
from absl import flags

from poldict.dictionary import Dictionary
from poldict.wiktionary_parser import parse_markup


FLAGS = flags.FLAGS
flags.DEFINE_string("dump_path", "", "Path to wikipedia dump.")
flags.DEFINE_string(
    "intermediate_dump",
    "",
    "Path for intermediate dump of Polish wikipedia pages. If file exists, will not regenerate.",
)
flags.DEFINE_string("output_path", "", "Path to output dictionary sqlite DB.")
flags.DEFINE_string("allow_list", "", "If specified, a file containing words to allow.")


def extract_polish_text(text):
    languages = []
    p = re.compile(r"==Polish==\n((.|\n)*?)(==[\w-]+==\n|$)")
    m = p.search(text)
    if m is None:
        raise KeyError("no polish text found")
    return m.group(1)


def dump_failed_text(title, text):
    output_file = Path("/tmp/wiktionary/" + title)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(text)


def extract_polish_pages(dump_path, output_path, allow_list):
    print(f"processing wiktionary dump at {dump_path}")

    allowed = set()
    if allow_list:
        words = [line.split(";")[0] for line in open(allow_list).readlines()[1:]]
        for word in words:
            allowed.add(word)

    db = dbm.open(output_path, "c")
    with bz2.open(dump_path, "rb") as f:
        namespace_str = "http://www.mediawiki.org/xml/export-0.11/"
        namespaces = {None: namespace_str}
        page_nums = 0
        for _, page_element in etree.iterparse(f, tag=f"{{{namespace_str}}}page"):
            title = page_element.findtext("title", "", namespaces)
            text = page_element.findtext("revision/text", "", namespaces)

            # Skip pages that don't have any Polish definitions.
            if "==Polish==" not in text:
                continue

            # Skip pages that are not in the allow list.
            if allowed and title.lower() not in allowed:
                continue

            # Skip thesaurus words.
            if title.startswith("Thesaurus:"):
                continue

            try:
                polish_text = extract_polish_text(text)
                db[title] = polish_text
            except KeyError:
                print(f"ERROR: Extraction failed for '{title}'")
                dump_failed_text(title, text)

            # Clear the element to save memory.
            page_element.clear()
            # Also eliminate now-empty references from the root node to elem
            for ancestor in page_element.xpath("ancestor-or-self::*"):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]

            page_nums += 1
            if page_nums % 1000 == 0:
                print(f"  ... {page_nums} raw polish pages collected")
        if page_nums % 1000 != 0:
            print(f"  {page_nums} raw polish pages collected, done.")
    db.close()


def extract_words(intermediate_dump, output_path):
    dictionary = Dictionary(output_path)
    dictionary.create()
    with dbm.open(intermediate_dump) as db:
        words_and_protos = []
        for key in db.keys():
            word = key.decode("utf-8")
            try:
                proto = parse_markup(word, db[key].decode("utf-8"))
            except Exception as e:
                print("---> word:", word)
                raise e
            if not proto.meanings:
                continue
            words_and_protos.append((word, proto))
        dictionary.insert_many(words_and_protos)
        print(f"Inserted {len(words_and_protos)} words into the dictionary.")
    dictionary.close()


def main(argv):
    del argv
    if not os.path.exists(FLAGS.intermediate_dump + ".db"):
        extract_polish_pages(FLAGS.dump_path, FLAGS.intermediate_dump, FLAGS.allow_list)
    extract_words(FLAGS.intermediate_dump, FLAGS.output_path)


if __name__ == "__main__":
    app.run(main)
