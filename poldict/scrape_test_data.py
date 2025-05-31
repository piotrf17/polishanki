# python3 -m poldict.scrape_test_data --rescrape_all

import os.path
import sys

from absl import app
from absl import flags

from poldict import wiktionary_scraper

FLAGS = flags.FLAGS
flags.DEFINE_boolean("rescrape_all", False, "If true, rescrape all test cases")
flags.DEFINE_list(
    "words",
    ["biegać", "człowiek", "czerwony", "dom", "drzwi", "gość", "pobiec", "ja", "który"],
    "Words to scrape",
)


def main(argv):
    del argv
    for word in FLAGS.words:
        filename = f"poldict/testdata/{word}.html"
        if os.path.exists(filename) and not FLAGS.rescrape_all:
            continue
        print('Scraping html for "{}"'.format(word))
        html = wiktionary_scraper.get_html(word)
        open(filename, "w").write(html.decode("utf-8"))


if __name__ == "__main__":
    app.run(main)
