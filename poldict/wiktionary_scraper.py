"""Library to scrape inflected polish word forms from wiktionary.

Typical usage is:
  word = wiktionary_scraper.get_forms('drzwi')
"""

import logging
import re
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import NavigableString

from poldict import inflection_pb2

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
}

# If set to true, then the fetched data will be saved to disk, and loaded
# from there on the next run. Useful for debugging and fixing scraping code.
DEBUG = True


def get_html(word, debug=False):
    """Scrapes wiktionary for a word and returns a string with the html."""
    url = "http://en.wiktionary.org/wiki/" + urllib.parse.quote(word)
    request = urllib.request.Request(url, headers=HEADERS)
    if debug:
        logging.info("Scraper debug mode is enabled")
        try:
            return open("/tmp/scraped_data.txt").read()
        except FileNotFoundError:
            logging.info("Saved scrape not found, fetching live.")
    data = urllib.request.urlopen(request).read()
    if debug:
        open("/tmp/scraped_data.txt", "w").write(data.decode("utf-8"))
    return data


class ParseNode(object):

    def __init__(self, title, depth):
        self.title = title
        self.depth = depth
        self.tags = []
        self.children = []
        self.parent = None
        self.next = None

    def find_all(self, title):
        result = []
        if self.title == title:
            result.append(self)
        for child in self.children:
            result.extend(child.find_all(title))
        return result

    def find(self, title):
        if self.title == title:
            return self
        for child in self.children:
            result = child.find(title)
            if result:
                return result
        return None

    def print(self):
        print(" " * (self.depth - 2) + self.title)
        for child in self.children:
            child.print()

    def find_tag(self, name, cl=None):
        for tag in self.tags:
            if tag.name == name:
                if cl is not None and cl in tag.attrs["class"]:
                    return tag
            result = tag.find(name, cl)
            if result is not None:
                return result
        return None


def _parse_html(soup):
    current_tag = None
    for lang_heading in soup.find_all("h2"):
        headline = lang_heading.find("span", "mw-headline")
        if headline is None:
            continue
        if headline.string.strip() == "Polish":
            current_tag = lang_heading
            break
    if not current_tag:
        raise KeyError("no Polish definition")

    root = ParseNode("Polish", 2)
    node = root

    while current_tag.next_sibling is not None:
        current_tag = current_tag.next_sibling

        # From the documentation, this shouldn't be possible, but it seems
        # to happen in practice.
        if current_tag.name is None:
            continue

        if len(current_tag.name) == 2 and current_tag.name[0] == "h":
            depth = int(current_tag.name[1])

            # Break if another language starts.
            if depth == 2:
                break

            next_node = ParseNode(current_tag.span.string.strip(), depth)
            if depth > node.depth:
                node.children.append(next_node)
                next_node.parent = node
                node = next_node
            else:
                diff = node.depth - depth
                while diff > 0:
                    node = node.parent
                    diff -= 1
                next_node.parent = node.parent
                next_node.parent.children.append(next_node)
                node.next = next_node
                node = next_node
        else:
            node.tags.append(current_tag)

    return root


def _add_cases_form(form, text, proto):
    if form == "nominative":
        proto.nominative = text
    elif form == "genitive":
        proto.genitive = text
    elif form == "dative":
        proto.dative = text
    elif form == "accusative":
        proto.accusative = text
    elif form == "instrumental":
        proto.instrumental = text
    elif form == "locative":
        proto.locative = text
    elif form == "vocative":
        proto.vocative = text


def _span_to_text(span):
    form = []
    for child in span.descendants:
        if type(child) == NavigableString:
            part = child.strip()
            if part:
                form.append(part)
    form = " ".join(form)
    form.strip()
    return form


def _parse_noun_inflection_table(table, noun_declension):
    rows = table.find_all("tr")
    if not rows:
        raise KeyError("declension table empty")

    # Determine if the noun has singular and/or plural forms.
    headers = rows[0].find_all("th")
    singular = None
    plural = None
    if len(headers) > 2:
        singular = noun_declension.singular
        plural = noun_declension.plural
    elif headers[1].string.strip() == "singular":
        singular = noun_declension.singular
    elif headers[1].string.strip() == "plural":
        plural = noun_declension.plural
    else:
        raise KeyError("noun has no singular or plural")

    for row in rows[1:]:
        form = row.th.string.strip()
        texts = row.find_all("td")
        if singular:
            _add_cases_form(form, _span_to_text(texts[0].span), singular)
            if plural:
                _add_cases_form(form, _span_to_text(texts[1].span), plural)
        elif plural:
            _add_cases_form(form, _span_to_text(texts[0]), plural)


def _parse_verb_person_forms(row, person):
    for entry in row.find_all("td"):
        num_entries = 1
        if "colspan" in entry.attrs:
            num_entries = int(entry["colspan"])
        form = _span_to_text(entry.span)
        for i in range(num_entries):
            person.append(form)


def _parse_verb_inflection_table(table, verb_declension):
    rows = table.find_all("tr")
    if not rows:
        raise KeyError("conjugation table empty")

    current_tense = None

    for row in rows:
        if not "title" in row.th.attrs:
            continue

        title = row.th["title"]
        if title == "czas teraźniejszy":
            current_tense = verb_declension.present
            _parse_verb_person_forms(row, current_tense.first)
        elif title == "czas przeszły":
            current_tense = verb_declension.past
            _parse_verb_person_forms(row, current_tense.first)
        elif title.startswith("czas przyszły"):
            current_tense = verb_declension.future
            _parse_verb_person_forms(row, current_tense.first)
        elif title == "tryb przypuszczający":
            current_tense = verb_declension.conditional
            _parse_verb_person_forms(row, current_tense.first)
        elif title == "tryb rozkazujący":
            current_tense = verb_declension.imperative
            _parse_verb_person_forms(row, current_tense.first)
        elif title == "imiesłów przymiotnikowy czynny":
            _parse_verb_person_forms(row, verb_declension.active_adjectival_participle)
        elif title == "imiesłów przysłówkowy współczesny":
            _parse_verb_person_forms(
                row, verb_declension.contemporary_adverbial_participle
            )
        elif title == "imiesłów przysłówkowy uprzedni":
            _parse_verb_person_forms(row, verb_declension.anterior_adverbial_participle)
        elif title == "rzeczownik odczasownikowy":
            _parse_verb_person_forms(row, verb_declension.verbal_noun)
        elif title.startswith("druga osoba"):
            assert current_tense is not None
            _parse_verb_person_forms(row, current_tense.second)
        elif title.startswith("trzecia osoba"):
            assert current_tense is not None
            _parse_verb_person_forms(row, current_tense.third)
        elif title.startswith("forma bezosobowa"):
            assert current_tense is not None
            _parse_verb_person_forms(row, current_tense.impersonal)


def _parse_adjective_inflection_table(table, adjective_declension):
    rows = table.find_all("tr")
    if not rows:
        raise KeyError("declension table empty")
    cases = [
        adjective_declension.masculine_animate,
        adjective_declension.masculine_inanimate,
        adjective_declension.feminine,
        adjective_declension.neuter,
        adjective_declension.plural_virile,
        adjective_declension.plural_nonvirile,
    ]
    for row in rows[2:]:
        form = row.th.string.strip()
        cases_idx = 0
        for entry in row.find_all("td"):
            num_entries = 1
            if "colspan" in entry.attrs:
                num_entries = int(entry["colspan"])
            text = _span_to_text(entry.span)
            for i in range(num_entries):
                _add_cases_form(form, text, cases[cases_idx])
                cases_idx += 1


def get_forms_from_html(word, html):
    soup = BeautifulSoup(html, features="lxml")
    parse_tree = _parse_html(soup)

    proto = inflection_pb2.Word()
    proto.word = word

    nouns = parse_tree.find_all("Noun")
    for noun in nouns:
        meaning = inflection_pb2.Meaning()
        meaning.part_of_speech = inflection_pb2.Meaning.kNoun
        declension = noun.find("Declension")
        if declension is None:
            continue
        inflection_table = declension.find_tag("table", "inflection-table")
        assert inflection_table is not None
        _parse_noun_inflection_table(inflection_table, meaning.noun)
        proto.meanings.append(meaning)

    verbs = parse_tree.find_all("Verb")
    for verb in verbs:
        meaning = inflection_pb2.Meaning()
        meaning.part_of_speech = inflection_pb2.Meaning.kVerb
        conjugation = verb.find("Conjugation")
        if conjugation is None:
            continue
        inflection_table = conjugation.find_tag("table", "inflection-table")
        assert inflection_table is not None
        _parse_verb_inflection_table(inflection_table, meaning.verb)
        proto.meanings.append(meaning)

    adjectives = parse_tree.find_all("Adjective")
    for adjective in adjectives:
        meaning = inflection_pb2.Meaning()
        meaning.part_of_speech = inflection_pb2.Meaning.kAdjective
        declension = adjective.find("Declension")
        if declension is None:
            continue
        inflection_table = declension.find_tag("table", "inflection-table")
        assert inflection_table is not None
        _parse_adjective_inflection_table(inflection_table, meaning.adjective)
        proto.meanings.append(meaning)

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
    print(get_forms("biegać"))
