import os.path
import sys

from absl import app
from absl import flags

import wiktionary_scraper

FLAGS = flags.FLAGS
flags.DEFINE_boolean("rescrape_all", False, "If true, rescrape all test cases")
flags.DEFINE_list(
    "words", ["biegać", "czerwony", "drzwi", "gość", "pobiec"], "Words to scrape"
)


def main(argv):
    del argv
    for word in FLAGS.words:
        filename = f"testdata/{word}.html"
        if os.path.exists(filename) and not FLAGS.rescrape_all:
            continue
        print('Scraping html for "{}"'.format(word))
        html = wiktionary_scraper.get_html(word)
        open(filename, "w").write(html.decode("utf-8"))


if __name__ == "__main__":
    app.run(main)
