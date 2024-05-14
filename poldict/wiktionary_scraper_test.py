import unittest

import wiktionary_scraper

def get_forms(word):
    with open('testdata/' + word + '.html') as f:
        html = f.read()
    return wiktionary_scraper.get_forms_from_html(word, html)

class TestWiktionaryScraper(unittest.TestCase):

    def test_noun(self):
        word = get_forms('gość')
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof('inflection'), 'noun')

        self.assertEqual(m.noun.singular.nominative, 'gość')
        self.assertEqual(m.noun.singular.genitive, "gościa")
        self.assertEqual(m.noun.singular.dative, "gościowi")
        self.assertEqual(m.noun.singular.accusative, "gościa")
        self.assertEqual(m.noun.singular.instrumental, "gościem")
        self.assertEqual(m.noun.singular.locative, "gościu")
        self.assertEqual(m.noun.singular.vocative, "gościu")

        self.assertEqual(m.noun.plural.nominative, "goście")
        self.assertEqual(m.noun.plural.genitive, "gości")
        self.assertEqual(m.noun.plural.dative, "gościom")
        self.assertEqual(m.noun.plural.accusative, "gości")
        self.assertEqual(m.noun.plural.instrumental, "gośćmi")
        self.assertEqual(m.noun.plural.locative, "gościach")
        self.assertEqual(m.noun.plural.vocative, "goście")
        
    
    def test_plural_only_noun(self):
        word = get_forms('drzwi')
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof('inflection'), 'noun')
        self.assertFalse(m.noun.HasField('singular'))
                     
        self.assertEqual(m.noun.plural.nominative, 'drzwi')
        self.assertEqual(m.noun.plural.genitive, 'drzwi')
        self.assertEqual(m.noun.plural.dative, 'drzwiom')
        self.assertEqual(m.noun.plural.accusative, 'drzwi')
        self.assertEqual(m.noun.plural.instrumental, 'drzwiami')
        self.assertEqual(m.noun.plural.locative, 'drzwiach')
        self.assertEqual(m.noun.plural.vocative, 'drzwi')


    def test_imperfect_verb(self):
        word = get_forms('biegać')
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof('inflection'), 'verb')
        self.assertEqual(m.verb.present.first, ['biegam'] * 3 + ['biegamy'] * 2)
        self.assertEqual(m.verb.present.second, ['biegasz'] * 3 + ['biegacie'] * 2)
        self.assertEqual(m.verb.present.third, ['biega'] * 3 + ['biegają'] * 2)
        self.assertEqual(m.verb.present.impersonal, ['biega się'] * 5)
        self.assertEqual(m.verb.past.first,
                         ['biegałem', 'biegałam', 'biegałom', 'biegaliśmy', 'biegałyśmy'])
        self.assertEqual(m.verb.past.second,
                         ['biegałeś', 'biegałaś', 'biegałoś', 'biegaliście', 'biegałyście'])
        self.assertEqual(m.verb.past.third,
                         ['biegał',	'biegała', 'biegało',	'biegali', 'biegały'])
        self.assertEqual(m.verb.past.impersonal, ['biegano'] * 5)
        self.assertEqual(m.verb.future.first,
                         ['będę biegał', 'będę biegała', 'będę biegało',
                          'będziemy biegali', 'będziemy biegały'])
        self.assertEqual(m.verb.future.second,
                         ['będziesz biegał', 'będziesz biegała', 'będziesz biegało',
                          'będziecie biegali', 'będziecie biegały'])
        self.assertEqual(m.verb.future.third,
                         ['będzie biegał', 'będzie biegała', 'będzie biegało',
                          'będą biegali', 'będą biegały'])
        self.assertEqual(m.verb.future.impersonal, ['będzie biegać się'] * 5)
        self.assertEqual(m.verb.conditional.first,
                         ['biegałbym', 'biegałabym', 'biegałobym',
                          'biegalibyśmy', 'biegałybyśmy'])
        self.assertEqual(m.verb.conditional.second,
                         ['biegałbyś', 'biegałabyś', 'biegałobyś',
                          'biegalibyście', 'biegałybyście'])
        self.assertEqual(m.verb.conditional.third,
                         ['biegałby', 'biegałaby', 'biegałoby', 'biegaliby', 'biegałyby'])
        self.assertEqual(m.verb.conditional.impersonal, ['biegano by'] * 5)
        self.assertEqual(m.verb.imperative.first,
                         ['niech biegam'] * 3 + ['biegajmy'] * 2)
        self.assertEqual(m.verb.imperative.second,
                         ['biegaj'] * 3 + ['biegajcie'] * 2)
        self.assertEqual(m.verb.imperative.third,
                         ['niech biega'] * 3 + ['niech biegają'] * 2)
        self.assertEqual(m.verb.active_adjectival_participle,
                         ['biegający', 'biegająca',	'biegające', 'biegający',	'biegające'])
        self.assertEqual(m.verb.contemporary_adverbial_participle, ['biegając'] * 5)
        self.assertEqual(m.verb.anterior_adverbial_participle, [])
        self.assertEqual(m.verb.verbal_noun, ['bieganie'] * 5)


    def test_perfect_verb(self):
        word = get_forms('pobiec')
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof('inflection'), 'verb')
        self.assertFalse(m.verb.HasField('present'))
        self.assertEqual(m.verb.future.first, ['pobiegnę'] * 3 + ['pobiegniemy'] * 2)
        self.assertEqual(m.verb.future.second, ['pobiegniesz'] * 3 + ['pobiegniecie'] * 2)
        self.assertEqual(m.verb.future.third, ['pobiegnie'] * 3 + ['pobiegną'] * 2)
        self.assertEqual(m.verb.future.impersonal, ['pobiegnie się'] * 5)
        self.assertEqual(m.verb.past.first,
                         ['pobiegłem', 'pobiegłam', 'pobiegłom', 'pobiegliśmy', 'pobiegłyśmy'])
        self.assertEqual(m.verb.past.second,
                         ['pobiegłeś', 'pobiegłaś', 'pobiegłoś', 'pobiegliście', 'pobiegłyście'])
        self.assertEqual(m.verb.past.third,
                         ['pobiegł', 'pobiegła', 'pobiegło', 'pobiegli', 'pobiegły'])
        self.assertEqual(m.verb.past.impersonal, ['pobiegnięto'] * 5)
        self.assertEqual(m.verb.conditional.first,
                         ['pobiegłbym', 'pobiegłabym', 'pobiegłobym',
                          'pobieglibyśmy', 'pobiegłybyśmy'])
        self.assertEqual(m.verb.conditional.second,
                         ['pobiegłbyś', 'pobiegłabyś', 'pobiegłobyś',
                          'pobieglibyście', 'pobiegłybyście'])
        self.assertEqual(m.verb.conditional.third,
                         ['pobiegłby', 'pobiegłaby', 'pobiegłoby',
                          'pobiegliby', 'pobiegłyby'])
        self.assertEqual(m.verb.conditional.impersonal, ['pobiegnięto by'] * 5)
        self.assertEqual(m.verb.imperative.first,
                         ['niech pobiegnę'] * 3 + ['pobiegnijmy'] * 2)
        self.assertEqual(m.verb.imperative.second,
                         ['pobiegnij'] * 3 + ['pobiegnijcie'] * 2)
        self.assertEqual(m.verb.imperative.third,
                         ['niech pobiegnie'] * 3 + ['niech pobiegną'] * 2)
        self.assertEqual(m.verb.active_adjectival_participle, [])
        self.assertEqual(m.verb.contemporary_adverbial_participle, [])
        self.assertEqual(m.verb.anterior_adverbial_participle, ['pobiegłszy'] * 5)
        self.assertEqual(m.verb.verbal_noun, ['pobiegnięcie'] * 5)


if __name__ == '__main__':
    unittest.main()
