"""Library to scrape inflected polish word forms from wiktionary.

Typical usage is:
  word = wiktionary_scraper.get_forms('drzwi')
"""


import logging
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import NavigableString

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
            return 'noun', table
        if table.find_all('th', title='liczba pojedyncza'):
            return 'verb', table

    return 'unk', None


def _add_noun_form(form, text, proto):
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


def _parse_noun_inflection_table(table, noun_declension):
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
            _add_noun_form(form, texts[0].span.string.strip(), singular)
            if plural:
                _add_noun_form(form, texts[1].span.string.strip(), plural)
        elif plural:
            _add_noun_form(form, texts[0].span.string.strip(), plural)


def _parse_verb_person_forms(row, person):
    for entry in row.find_all('td'):
        num_entries = 1;
        if 'colspan' in entry.attrs:
            num_entries = int(entry['colspan'])
        form = []
        for child in entry.span.descendants:
            if type(child) == NavigableString:
                part = child.strip()
                if part:
                    form.append(part)
        form = ' '.join(form)
        for i in range(num_entries):
            person.append(form.strip())


def _parse_verb_inflection_table(table, verb_declension):
    rows = table.find_all('tr')
    if not rows:
        raise KeyError('conjugation table empty')

    current_tense = None

    for row in rows:
        if not 'title' in row.th.attrs:
            continue

        title = row.th['title']
        if title == 'czas teraźniejszy':
            current_tense = verb_declension.present
            _parse_verb_person_forms(row, current_tense.first)
        elif title == 'czas przeszły':
            current_tense = verb_declension.past
            _parse_verb_person_forms(row, current_tense.first)
        elif title == 'czas przyszły':
            current_tense = verb_declension.future
            _parse_verb_person_forms(row, current_tense.first)
        elif title == 'tryb przypuszczający':
            current_tense = verb_declension.conditional
            _parse_verb_person_forms(row, current_tense.first)
        elif title == 'tryb rozkazujący':
            current_tense = verb_declension.imperative
            _parse_verb_person_forms(row, current_tense.first)
        elif title == 'imiesłów przymiotnikowy czynny':
            _parse_verb_person_forms(row, verb_declension.active_adjectival_participle)
        elif title == 'imiesłów przysłówkowy współczesny':
            _parse_verb_person_forms(row, verb_declension.contemporary_adverbial_participle)
        elif title == 'rzeczownik odczasownikowy':
            _parse_verb_person_forms(row, verb_declension.verbal_noun)            
        elif title.startswith('druga osoba'):
            assert current_tense is not None
            _parse_verb_person_forms(row, current_tense.second)
        elif title.startswith('trzecia osoba'):
            assert current_tense is not None
            _parse_verb_person_forms(row, current_tense.third)
        elif title.startswith('forma bezosobowa'):
            assert current_tense is not None
            _parse_verb_person_forms(row, current_tense.impersonal)


def get_forms_from_html(word, html):
    soup = BeautifulSoup(html, features="lxml")
    table_type, inflection_table = _find_polish_inflection_table(soup)

    if inflection_table == None:
        raise KeyError('no inflection table found')

    proto = inflection_pb2.Word()
    proto.word = word
    if table_type == 'noun':
        _parse_noun_inflection_table(inflection_table, proto.noun)
    elif table_type == 'verb':
        _parse_verb_inflection_table(inflection_table, proto.verb)

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
    print(get_forms('biegać'))
