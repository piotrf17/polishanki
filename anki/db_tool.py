import csv
import os.path
import sys

from absl import app
from absl import flags

import note_db
import note_pb2

FLAGS = flags.FLAGS
flags.DEFINE_string("db_path", "data/anki.sqlite", "Path to anki sqlite db.")
flags.DEFINE_string(
    "import_csv", "", "If specified, path of csv to import into the db."
)


def confirm_command(db_path):
    if os.path.exists(db_path):
        print(f"DB exists at 'db_path', confirm overwrite?")
        choice = input("(y/N)--> ")
        if choice.upper() != "Y":
            print("Exiting without change.")
            sys.exit()


def import_csv(db_path, csv_path):
    print(f"Importing anki cards from '{csv_path}' to '{db_path}'")
    confirm_command(db_path)
    db = note_db.NoteDb(db_path)
    db.create()
    num_notes = 0
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file, delimiter=";")
        for row in reader:
            note = note_pb2.Note()
            try:
                note.id = int(row[0])
            except ValueError:
                note.id
            note.front = row[1]
            note.hint = row[3]
            note.word = row[4]
            note.back = row[5]
            note.extra_info = row[6]

            # Don't include grammar cards, this card creator tool only
            # deals with cards specifically tied to a word.
            if not note.word:
                continue

            db.insert_note_with_id(note)
            num_notes += 1
    db.close()
    print(f"Imported {num_notes} notes.")


def main(argv):
    del argv
    if FLAGS.import_csv:
        import_csv(FLAGS.db_path, FLAGS.import_csv)


if __name__ == "__main__":
    app.run(main)
