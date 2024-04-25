import unittest

import wiktionary_scraper

def get_forms(word):
    with open('testdata/' + word + '.html') as f:
        html = f.read()
    return wiktionary_scraper.get_forms_from_html(word, html)

class TestWiktionaryScraper(unittest.TestCase):

    def test_noun(self):
        word = get_forms('gość')
        self.assertEqual(word.WhichOneof('inflection'), 'noun')

        self.assertEqual(word.noun.singular.nominative, 'gość')
        self.assertEqual(word.noun.singular.genitive, "gościa")
        self.assertEqual(word.noun.singular.dative, "gościowi")
        self.assertEqual(word.noun.singular.accusative, "gościa")
        self.assertEqual(word.noun.singular.instrumental, "gościem")
        self.assertEqual(word.noun.singular.locative, "gościu")
        self.assertEqual(word.noun.singular.vocative, "gościu")

        self.assertEqual(word.noun.plural.nominative, "goście")
        self.assertEqual(word.noun.plural.genitive, "gości")
        self.assertEqual(word.noun.plural.dative, "gościom")
        self.assertEqual(word.noun.plural.accusative, "gości")
        self.assertEqual(word.noun.plural.instrumental, "gośćmi")
        self.assertEqual(word.noun.plural.locative, "gościach")
        self.assertEqual(word.noun.plural.vocative, "goście")
        
    
    def test_plural_only_noun(self):
        word = get_forms('drzwi')
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
