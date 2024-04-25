import unittest

import wiktionary_scraper

class TestWiktionaryScraper(unittest.TestCase):
    
    def test_plural_only_noun(self):
        with open('testdata/drzwi.html') as f:
            html = f.read()
        word = wiktionary_scraper.get_forms_from_html('drzwi', html)
        self.assertEqual(word.WhichOneof('inflection'), 'noun')
        self.assertFalse(word.noun.HasField('singular'))
        self.assertEqual(word.noun.plural.nominative, 'drzwi')
        self.assertEqual(word.noun.plural.genitive, 'drzwi')
        self.assertEqual(word.noun.plural.dative, 'drzwiom')
        self.assertEqual(word.noun.plural.accusative, 'drzwi')
        self.assertEqual(word.noun.plural.instrumental, 'drzwiami')
        self.assertEqual(word.noun.plural.locative, 'drzwiach')
        self.assertEqual(word.noun.plural.vocative, 'drzwi')

if __name__ == '__main__':
    unittest.main()
