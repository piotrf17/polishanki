import os.path
import unittest

from poldict import wiktionary_scraper


def get_forms(word):
    filename = os.path.join(os.path.dirname(__file__), f"testdata/{word}.html")
    with open(filename) as f:
        html = f.read()
    return wiktionary_scraper.get_forms_from_html(word, html)


class TestWiktionaryScraper(unittest.TestCase):

    def _check_cases(self, cases, expected):
        self.assertEqual(cases.nominative, expected[0])
        self.assertEqual(cases.genitive, expected[1])
        self.assertEqual(cases.dative, expected[2])
        self.assertEqual(cases.accusative, expected[3])
        self.assertEqual(cases.instrumental, expected[4])
        self.assertEqual(cases.locative, expected[5])
        self.assertEqual(cases.vocative, expected[6])

    def test_noun(self):
        word = get_forms("gość")
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof("inflection"), "noun")
        self._check_cases(
            m.noun.singular,
            ["gość", "gościa", "gościowi", "gościa", "gościem", "gościu", "gościu"],
        )
        self._check_cases(
            m.noun.plural,
            ["goście", "gości", "gościom", "gości", "gośćmi", "gościach", "goście"],
        )

    def test_plural_only_noun(self):
        word = get_forms("drzwi")
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof("inflection"), "noun")
        self.assertFalse(m.noun.HasField("singular"))
        self._check_cases(
            m.noun.plural,
            ["drzwi", "drzwi", "drzwiom", "drzwi", "drzwiami", "drzwiach", "drzwi"],
        )

    def test_noun_bug1(self):
        word = get_forms("człowiek")
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof("inflection"), "noun")
        self._check_cases(
            m.noun.singular,
            [
                "człowiek",
                "człowieka",
                "człowiekowi",
                "człowieka",
                "człowiekiem",
                "człowieku",
                "człowiecze / człowieku",
            ],
        )
        self._check_cases(
            m.noun.plural,
            ["ludzie", "ludzi", "ludziom", "ludzi", "ludźmi", "ludziach", "ludzie"],
        )

    def test_imperfect_verb(self):
        word = get_forms("biegać")
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof("inflection"), "verb")
        self.assertEqual(m.verb.present.first, ["biegam"] * 3 + ["biegamy"] * 2)
        self.assertEqual(m.verb.present.second, ["biegasz"] * 3 + ["biegacie"] * 2)
        self.assertEqual(m.verb.present.third, ["biega"] * 3 + ["biegają"] * 2)
        self.assertEqual(m.verb.present.impersonal, ["biega się"] * 5)
        self.assertEqual(
            m.verb.past.first,
            ["biegałem", "biegałam", "biegałom", "biegaliśmy", "biegałyśmy"],
        )
        self.assertEqual(
            m.verb.past.second,
            ["biegałeś", "biegałaś", "biegałoś", "biegaliście", "biegałyście"],
        )
        self.assertEqual(
            m.verb.past.third, ["biegał", "biegała", "biegało", "biegali", "biegały"]
        )
        self.assertEqual(m.verb.past.impersonal, ["biegano"] * 5)
        self.assertEqual(
            m.verb.future.first,
            [
                "będę biegał",
                "będę biegała",
                "będę biegało",
                "będziemy biegali",
                "będziemy biegały",
            ],
        )
        self.assertEqual(
            m.verb.future.second,
            [
                "będziesz biegał",
                "będziesz biegała",
                "będziesz biegało",
                "będziecie biegali",
                "będziecie biegały",
            ],
        )
        self.assertEqual(
            m.verb.future.third,
            [
                "będzie biegał",
                "będzie biegała",
                "będzie biegało",
                "będą biegali",
                "będą biegały",
            ],
        )
        self.assertEqual(m.verb.future.impersonal, ["będzie biegać się"] * 5)
        self.assertEqual(
            m.verb.conditional.first,
            ["biegałbym", "biegałabym", "biegałobym", "biegalibyśmy", "biegałybyśmy"],
        )
        self.assertEqual(
            m.verb.conditional.second,
            ["biegałbyś", "biegałabyś", "biegałobyś", "biegalibyście", "biegałybyście"],
        )
        self.assertEqual(
            m.verb.conditional.third,
            ["biegałby", "biegałaby", "biegałoby", "biegaliby", "biegałyby"],
        )
        self.assertEqual(m.verb.conditional.impersonal, ["biegano by"] * 5)
        self.assertEqual(
            m.verb.imperative.first, ["niech biegam"] * 3 + ["biegajmy"] * 2
        )
        self.assertEqual(m.verb.imperative.second, ["biegaj"] * 3 + ["biegajcie"] * 2)
        self.assertEqual(
            m.verb.imperative.third, ["niech biega"] * 3 + ["niech biegają"] * 2
        )
        self.assertEqual(
            m.verb.active_adjectival_participle,
            ["biegający", "biegająca", "biegające", "biegający", "biegające"],
        )
        self.assertEqual(m.verb.contemporary_adverbial_participle, ["biegając"] * 5)
        self.assertEqual(m.verb.anterior_adverbial_participle, [])
        self.assertEqual(m.verb.verbal_noun, ["bieganie"] * 5)

    def test_perfect_verb(self):
        word = get_forms("pobiec")
        self.assertEqual(len(word.meanings), 1)
        m = word.meanings[0]
        self.assertEqual(m.WhichOneof("inflection"), "verb")
        self.assertFalse(m.verb.HasField("present"))
        self.assertEqual(m.verb.future.first, ["pobiegnę"] * 3 + ["pobiegniemy"] * 2)
        self.assertEqual(
            m.verb.future.second, ["pobiegniesz"] * 3 + ["pobiegniecie"] * 2
        )
        self.assertEqual(m.verb.future.third, ["pobiegnie"] * 3 + ["pobiegną"] * 2)
        self.assertEqual(m.verb.future.impersonal, ["pobiegnie się"] * 5)
        self.assertEqual(
            m.verb.past.first,
            ["pobiegłem", "pobiegłam", "pobiegłom", "pobiegliśmy", "pobiegłyśmy"],
        )
        self.assertEqual(
            m.verb.past.second,
            ["pobiegłeś", "pobiegłaś", "pobiegłoś", "pobiegliście", "pobiegłyście"],
        )
        self.assertEqual(
            m.verb.past.third,
            ["pobiegł", "pobiegła", "pobiegło", "pobiegli", "pobiegły"],
        )
        self.assertEqual(m.verb.past.impersonal, ["pobiegnięto"] * 5)
        self.assertEqual(
            m.verb.conditional.first,
            [
                "pobiegłbym",
                "pobiegłabym",
                "pobiegłobym",
                "pobieglibyśmy",
                "pobiegłybyśmy",
            ],
        )
        self.assertEqual(
            m.verb.conditional.second,
            [
                "pobiegłbyś",
                "pobiegłabyś",
                "pobiegłobyś",
                "pobieglibyście",
                "pobiegłybyście",
            ],
        )
        self.assertEqual(
            m.verb.conditional.third,
            ["pobiegłby", "pobiegłaby", "pobiegłoby", "pobiegliby", "pobiegłyby"],
        )
        self.assertEqual(m.verb.conditional.impersonal, ["pobiegnięto by"] * 5)
        self.assertEqual(
            m.verb.imperative.first, ["niech pobiegnę"] * 3 + ["pobiegnijmy"] * 2
        )
        self.assertEqual(
            m.verb.imperative.second, ["pobiegnij"] * 3 + ["pobiegnijcie"] * 2
        )
        self.assertEqual(
            m.verb.imperative.third, ["niech pobiegnie"] * 3 + ["niech pobiegną"] * 2
        )
        self.assertEqual(m.verb.active_adjectival_participle, [])
        self.assertEqual(m.verb.contemporary_adverbial_participle, [])
        self.assertEqual(m.verb.anterior_adverbial_participle, ["pobiegłszy"] * 5)
        self.assertEqual(m.verb.verbal_noun, ["pobiegnięcie"] * 5)

    def test_noun_and_adj(self):
        word = get_forms("czerwony")
        self.assertEqual(len(word.meanings), 2)

        m = word.meanings[0]
        self.assertEqual(m.WhichOneof("inflection"), "noun")
        self._check_cases(
            m.noun.singular,
            [
                "czerwony",
                "czerwonego",
                "czerwonemu",
                "czerwonego",
                "czerwonym",
                "czerwonym",
                "czerwony",
            ],
        )
        self._check_cases(
            m.noun.plural,
            [
                "czerwone",
                "czerwonych",
                "czerwonym",
                "czerwonych",
                "czerwonymi",
                "czerwonych",
                "czerwone",
            ],
        )

        m = word.meanings[1]
        self.assertEqual(m.WhichOneof("inflection"), "adjective")
        self._check_cases(
            m.adjective.masculine_animate,
            [
                "czerwony",
                "czerwonego",
                "czerwonemu",
                "czerwonego",
                "czerwonym",
                "czerwonym",
                "",
            ],
        )
        self._check_cases(
            m.adjective.masculine_inanimate,
            [
                "czerwony",
                "czerwonego",
                "czerwonemu",
                "czerwony",
                "czerwonym",
                "czerwonym",
                "",
            ],
        )
        self._check_cases(
            m.adjective.feminine,
            [
                "czerwona",
                "czerwonej",
                "czerwonej",
                "czerwoną",
                "czerwoną",
                "czerwonej",
                "",
            ],
        )
        self._check_cases(
            m.adjective.neuter,
            [
                "czerwone",
                "czerwonego",
                "czerwonemu",
                "czerwone",
                "czerwonym",
                "czerwonym",
                "",
            ],
        )
        self._check_cases(
            m.adjective.plural_virile,
            [
                "czerwoni",
                "czerwonych",
                "czerwonym",
                "czerwonych",
                "czerwonymi",
                "czerwonych",
                "",
            ],
        )
        self._check_cases(
            m.adjective.plural_nonvirile,
            [
                "czerwone",
                "czerwonych",
                "czerwonym",
                "czerwone",
                "czerwonymi",
                "czerwonych",
                "",
            ],
        )


if __name__ == "__main__":
    unittest.main()
