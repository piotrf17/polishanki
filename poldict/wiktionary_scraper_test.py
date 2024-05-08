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


    def test_imperfect_verb(self):
        word = get_forms('biegać')
        self.assertEqual(word.WhichOneof('inflection'), 'verb')
        self.assertEqual(word.verb.present.first, ['biegam'] * 3 + ['biegamy'] * 2)
        self.assertEqual(word.verb.present.second, ['biegasz'] * 3 + ['biegacie'] * 2)
        self.assertEqual(word.verb.present.third, ['biega'] * 3 + ['biegają'] * 2)
        self.assertEqual(word.verb.present.impersonal, ['biega się'] * 5)
        self.assertEqual(word.verb.past.first,
                         ['biegałem', 'biegałam', 'biegałom', 'biegaliśmy', 'biegałyśmy'])
        self.assertEqual(word.verb.past.second,
                         ['biegałeś', 'biegałaś', 'biegałoś', 'biegaliście', 'biegałyście'])
        self.assertEqual(word.verb.past.third,
                         ['biegał',	'biegała', 'biegało',	'biegali', 'biegały'])
        self.assertEqual(word.verb.past.impersonal, ['biegano'] * 5)
        self.assertEqual(word.verb.future.first,
                         ['będę biegał', 'będę biegała', 'będę biegało',
                          'będziemy biegali', 'będziemy biegały'])
        self.assertEqual(word.verb.future.second,
                         ['będziesz biegał', 'będziesz biegała', 'będziesz biegało',
                          'będziecie biegali', 'będziecie biegały'])
        self.assertEqual(word.verb.future.third,
                         ['będzie biegał', 'będzie biegała', 'będzie biegało',
                          'będą biegali', 'będą biegały'])
        self.assertEqual(word.verb.future.impersonal, ['będzie biegać się'] * 5)
        self.assertEqual(word.verb.conditional.first,
                         ['biegałbym', 'biegałabym', 'biegałobym',
                          'biegalibyśmy', 'biegałybyśmy'])
        self.assertEqual(word.verb.conditional.second,
                         ['biegałbyś', 'biegałabyś', 'biegałobyś',
                          'biegalibyście', 'biegałybyście'])
        self.assertEqual(word.verb.conditional.third,
                         ['biegałby', 'biegałaby', 'biegałoby', 'biegaliby', 'biegałyby'])
        self.assertEqual(word.verb.conditional.impersonal, ['biegano by'] * 5)
        self.assertEqual(word.verb.imperative.first,
                         ['niech biegam'] * 3 + ['biegajmy'] * 2)
        self.assertEqual(word.verb.imperative.second,
                         ['biegaj'] * 3 + ['biegajcie'] * 2)
        self.assertEqual(word.verb.imperative.third,
                         ['niech biega'] * 3 + ['niech biegają'] * 2)
        self.assertEqual(word.verb.active_adjectival_participle,
                         ['biegający', 'biegająca',	'biegające', 'biegający',	'biegające'])
        self.assertEqual(word.verb.contemporary_adverbial_participle, ['biegając'] * 5)
        self.assertEqual(word.verb.anterior_adverbial_participle, [])
        self.assertEqual(word.verb.verbal_noun, ['bieganie'] * 5)


    def test_perfect_verb(self):
        word = get_forms('pobiec')
        self.assertEqual(word.WhichOneof('inflection'), 'verb')
        self.assertFalse(word.verb.HasField('present'))
        self.assertEqual(word.verb.future.first, ['pobiegnę'] * 3 + ['pobiegniemy'] * 2)
        self.assertEqual(word.verb.future.second, ['pobiegniesz'] * 3 + ['pobiegniecie'] * 2)
        self.assertEqual(word.verb.future.third, ['pobiegnie'] * 3 + ['pobiegną'] * 2)
        self.assertEqual(word.verb.future.impersonal, ['pobiegnie się'] * 5)
        self.assertEqual(word.verb.past.first,
                         ['pobiegłem', 'pobiegłam', 'pobiegłom', 'pobiegliśmy', 'pobiegłyśmy'])
        self.assertEqual(word.verb.past.second,
                         ['pobiegłeś', 'pobiegłaś', 'pobiegłoś', 'pobiegliście', 'pobiegłyście'])
        self.assertEqual(word.verb.past.third,
                         ['pobiegł', 'pobiegła', 'pobiegło', 'pobiegli', 'pobiegły'])
        self.assertEqual(word.verb.past.impersonal, ['pobiegnięto'] * 5)
        self.assertEqual(word.verb.conditional.first,
                         ['pobiegłbym', 'pobiegłabym', 'pobiegłobym',
                          'pobieglibyśmy', 'pobiegłybyśmy'])
        self.assertEqual(word.verb.conditional.second,
                         ['pobiegłbyś', 'pobiegłabyś', 'pobiegłobyś',
                          'pobieglibyście', 'pobiegłybyście'])
        self.assertEqual(word.verb.conditional.third,
                         ['pobiegłby', 'pobiegłaby', 'pobiegłoby',
                          'pobiegliby', 'pobiegłyby'])
        self.assertEqual(word.verb.conditional.impersonal, ['pobiegnięto by'] * 5)
        self.assertEqual(word.verb.imperative.first,
                         ['niech pobiegnę'] * 3 + ['pobiegnijmy'] * 2)
        self.assertEqual(word.verb.imperative.second,
                         ['pobiegnij'] * 3 + ['pobiegnijcie'] * 2)
        self.assertEqual(word.verb.imperative.third,
                         ['niech pobiegnie'] * 3 + ['niech pobiegną'] * 2)
        self.assertEqual(word.verb.active_adjectival_participle, [])
        self.assertEqual(word.verb.contemporary_adverbial_participle, [])
        self.assertEqual(word.verb.anterior_adverbial_participle, ['pobiegłszy'] * 5)
        self.assertEqual(word.verb.verbal_noun, ['pobiegnięcie'] * 5)


if __name__ == '__main__':
    unittest.main()
