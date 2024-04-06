import logging
import urllib.request
from bs4 import BeautifulSoup

from poldict import inflection_pb2

HEADERS = {
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
}

# If set to true, then the fetched data will be saved to disk, and loaded
# from there on the next run. Useful for debugging and fixing scraping code.
DEBUG=True

def get_html(url):
    request = urllib.request.Request(url, headers=HEADERS)
    if DEBUG:
      logging.info('Scraper debug mode is enabled')
      try:
        return open('/tmp/scraped_data.txt').read()
      except FileNotFoundError:
        logging.info('Saved scrape not found, fetching live.')
    data = urllib.request.urlopen(request).read()
    if DEBUG:
      open('/tmp/scraped_data.txt', 'w').write(data.decode('utf-8'))
    return data


def get_polish_inflection(soup):
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
        
def get_forms(word):
    html = get_html('http://en.wiktionary.org/wiki/' + urllib.parse.quote(word))
    soup = BeautifulSoup(html, features="lxml")
    inflection_table = get_polish_inflection(soup)

    proto = inflection_pb2.Word()
    proto.word = word
    parse_inflection_table(inflection_table, proto.noun)

    print(proto)
    

if __name__ == "__main__":
#    get_forms('gość')
    get_forms('drzwi')
