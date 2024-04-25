import sys

import wiktionary_scraper

if __name__ == "__main__":
    word = sys.argv[1]
    print('Scraping html for "{}"'.format(word))
    html = wiktionary_scraper.get_html(word)
    open('testdata/' + word + '.html', 'w').write(html.decode('utf-8'))
