import re

from poldict import dictionary_pb2


class ParseNode(object):

    def __init__(self, title, depth):
        self.title = title
        self.depth = depth
        self.lines = []
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


def _build_parse_tree(page):
    root = ParseNode("Polish", 2)
    node = root

    heading_re = re.compile(r"(=+)(.+)\1")
    for line in page.split("\n"):
        m = heading_re.match(line)
        if m:
            depth = len(m.group(1))
            # Depth of less than 2 shouldn't happen, but sometimes the page extraction
            # code isn't perfect at isolating to Polish only.
            if depth <= 2:
                break
            title = m.group(2)

            next_node = ParseNode(title, depth)
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
            node.lines.append(line)

    return root


def _parse_gender(gender):
    if gender == "m-pr" or gender == "vr-p":
        return dictionary_pb2.Meaning.kMasculinePersonal
    elif gender == "m-anml" or gender == "m-anml-p":
        return dictionary_pb2.Meaning.kMasculineAnimate
    elif gender == "m-in" or gender == "nv-p" or gender == "m-in-p":
        return dictionary_pb2.Meaning.kMasculineInanimate
    elif gender == "f" or gender == "f-p":
        return dictionary_pb2.Meaning.kFeminine
    elif gender == "n":
        return dictionary_pb2.Meaning.kNeuter
    assert False, f"ERROR: unknown gender '{gender}'"


def _find_head(lines):
    ix = 0
    while ix < len(lines):
        if lines[ix].startswith("{{elements"):
            ix += 1
        if lines[ix].startswith("{{wp"):
            ix += 1
        if lines[ix].startswith("{{"):
            return lines[ix]
        ix += 1
    assert False, f"ERROR: failed to find head in: {lines}"


def _parse_template(template):
    assert template.startswith("{{")
    assert template.endswith("}}")
    parts = template[2:-2].split("|")
    if parts[0] == "lb":
        assert len(parts) > 2, parts
        return f"({parts[2]})"
    elif parts[0] == "gl":
        assert len(parts) > 1, parts
        return f"({parts[1]})"
    elif parts[0] == "verbal noun of":
        assert len(parts) > 2, parts
        return f"verbal noun of {parts[2]}"
    elif parts[0] == "w":
        assert len(parts) > 1, parts
        return parts[1]
    elif parts[0] == "l":
        assert len(parts) > 2, parts
        return parts[2]
    elif parts[0] == "+preo":
        if len(parts) > 4:
            return f"[+ {parts[2]} ({parts[3]}) = {parts[4][6:]}]"
        elif len(parts) == 4:
            return f"[+ {parts[2]} ({parts[3]})]"
        else:
            assert len(parts) == 3, parts
            return f"[+ {parts[2]} (object)]"
    elif parts[0] == "dim of" or parts[0] == "diminutive of":
        assert len(parts) > 2, parts
        return f"diminutive of {parts[2]}"
    elif parts[0] == "taxfmt":
        assert len(parts) > 1, parts
        return parts[1]
    return template


def _parse_definition(line):
    assert line.startswith("# ")
    line = line[2:]

    result = []

    # Render templates.
    template_re = re.compile(r"\{\{.+?\}\}")
    templates = template_re.findall(line)

    start_ix = 0
    for template in templates:
        tmpl_ix = line.find(template, start_ix)
        assert tmpl_ix > -1

        # Add in whatever came before the template.
        result.append(line[start_ix:tmpl_ix])

        result.append(_parse_template(template))

        start_ix = tmpl_ix + len(template)

    # Add in whatever came after the last template.
    result.append(line[start_ix:])
    result = "".join(result)

    # Remove link tags.
    result = result.replace("[[", "").replace("]]", "")

    return result


def _parse_noun(word, noun):
    if not noun.lines:
        return None

    meaning = dictionary_pb2.Meaning()
    meaning.part_of_speech = dictionary_pb2.Meaning.kNoun

    head = _find_head(noun.lines)
    template_re = re.compile(r"\{\{.+?\}\}")
    templates = template_re.findall(head)

    for template in templates:
        head_parts = template[2:-2].split("|")

        # Skip noun entries that are inflection forms, and not base words.
        if head_parts[0] == "head" or head_parts[0] == "head-lite":
            return None

        if head_parts[0] != "pl-noun":
            continue

        for gender in head_parts[1].split(","):
            # Skip nouns that have an unattested gender, usually these are wierd.
            if gender[-1] == "!":
                print(f"SKIPPING: noun {word} has unattested gender")
                return None
            meaning.gender.append(_parse_gender(gender))

    if not meaning.gender:
        print(f"SKIPPING: noun {word} has no gender")
        return None

    # Parse out definitions.
    for line in noun.lines:
        if line.startswith("# "):
            meaning.definition.append(_parse_definition(line))

    return meaning


def parse_markup(title, page):
    parse_tree = _build_parse_tree(page)

    proto = dictionary_pb2.Word()
    proto.word = title

    nouns = parse_tree.find_all("Noun")
    for noun in nouns:
        meaning = _parse_noun(title, noun)
        if meaning is None:
            continue
        proto.meanings.append(meaning)

    return proto
