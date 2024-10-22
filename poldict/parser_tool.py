import dbm

from absl import app
from absl import flags

from poldict.wiktionary_parser import parse_markup

FLAGS = flags.FLAGS
flags.DEFINE_string(
    "intermediate_dump",
    "",
    "Path to intermediate dump extracted by wiktionary_dump_to_db.",
)
flags.DEFINE_string("word", "", "Word to parse.")


def main(argv):
    word = FLAGS.word
    with dbm.open(FLAGS.intermediate_dump) as db:
        key = word.encode("utf-8")
        proto = parse_markup(word, db[key].decode("utf-8"))
        print(proto)


if __name__ == "__main__":
    app.run(main)
