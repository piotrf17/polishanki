"""Library to parse raw wiktionary mark-up into polish word data.
"""

import re

import inflection_pb2


def parse_markup(page):
    heading_re = re.compile(r'(=+)(.+)\1')
    for line in page.split('\n'):
        m = heading_re.match(line)
        if m:
            depth = len(m.group(1))
            assert depth > 2
            heading = m.group(2)
            print(depth, heading)


def get_forms(page):
    markup = parse_markup(page)
    
    proto = inflection_pb2.Word()
    return proto
