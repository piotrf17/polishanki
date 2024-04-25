"""Library to scrape inflected polish word forms from wiktionary.

Typical usage is:
  word = wiktionary_scraper.get_forms('drzwi')
"""


import logging
import urllib.request
from bs4 import BeautifulSoup

import inflection_pb2

HEADERS = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

# If set to true, then the fetched data will be saved to disk, and loaded
# from there on the next run. Useful for debugging and fixing scraping code.
DEBUG=True

def get_html(word, debug=False):
    """Scrapes wiktionary for a word and returns a string with the html."""
    url = 'http://en.wiktionary.org/wiki/' + urllib.parse.quote(word)
    request = urllib.request.Request(url, headers=HEADERS)
    if debug:
      logging.info('Scraper debug mode is enabled')
      try:
        return open('/tmp/scraped_data.txt').read()
      except FileNotFoundError:
        logging.info('Saved scrape not found, fetching live.')
    data = urllib.request.urlopen(request).read()
    if debug:
      open('/tmp/scraped_data.txt', 'w').write(data.decode('utf-8'))
    return data


def _find_polish_inflection_table(soup):
    tables = soup.find_all('table', 'inflection-table')
    for table in tables:
        if table.find_all('th', title='mianownik (kto? co?)'):
            return table


def add_noun_form(form, text, proto):
    if form == 'nominative':
        proto.nominative = text
    elif form == 'genitive':
        proto.genitive = text
    elif form == 'dative':
        proto.dative = text
    elif form == 'accusative':
        proto.accusative = text
    elif form == 'instrumental':
        proto.instrumental = text
    elif form == 'locative':
        proto.locative = text
    elif form == 'vocative':
        proto.vocative = text


def parse_inflection_table(table, noun_declension):
    rows = table.find_all('tr')
    if not rows:
        raise KeyError('declension table empty')

    # Determine if the noun has singular and/or plural forms.
    headers = rows[0].find_all('th')
    singular = None
    plural = None
    if len(headers) > 2:
        singular = noun_declension.singular
        plural = noun_declension.plural
    elif headers[1].string.strip() == 'singular':
        singular = noun_declension.singular
    elif headers[1].string.strip() == 'plural':
        plural = noun_declension.plural
    else:
        raise KeyError('noun has no singular or plural')

    for row in rows[1:]:
        form = row.th.string.strip()
        texts = row.find_all('td')
        if singular:
            add_noun_form(form, texts[0].span.string.strip(), singular)
            if plural:
                add_noun_form(form, texts[1].span.string.strip(), plural)
        elif plural:
            add_noun_form(form, texts[0].span.string.strip(), plural)


def get_forms_from_html(word, html):
    soup = BeautifulSoup(html, features="lxml")
    inflection_table = _find_polish_inflection_table(soup)

    proto = inflection_pb2.Word()
    proto.word = word
    parse_inflection_table(inflection_table, proto.noun)

    return proto


def get_forms(word):
    """Scrapes wiktionary for all inflected forms of the given word.

    Args:
        word: a string word to scrape

    Returns:
        An inflection_pb2.Word containing all inflected forms.
    """
    html = get_html(word, DEBUG)
    return get_forms_from_html(word, html)
    

if __name__ == "__main__":
#    get_forms('gość')
    print(get_forms('drzwi'))
