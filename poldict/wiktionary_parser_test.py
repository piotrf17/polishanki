import unittest

import wiktionary_parser


def get_forms(word):
    with open(f'testdata/{word}.md') as f:
        page = f.read()
    return wiktionary_parser.get_forms(page)


class TestWiktionaryParser(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
