import sys

from wiktionary_db import PageDb


TEST_WORDS = [
    'gość',
#    'rząd',
    ]


def extract_test_cases(db_path, words):
    db = PageDb(db_path)
    for word in words:
        page = db.get_page(word)
        path = f'testdata/{word}.md'
        open(path, 'w').write(page)


if __name__ == '__main__':
    db_path = sys.argv[1]
    extract_test_cases(db_path, TEST_WORDS)
