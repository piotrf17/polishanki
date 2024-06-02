import csv
import random
import sqlite3
import time

from anki import note_pb2

SCHEMA = """
DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
  id INTEGER PRIMARY KEY,
  word TEXT NOT NULL,
  note TEXT NOT NULL
);
"""


class NoteDb(object):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def create(self):
        """Drops any existing table and creates a new one."""
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    def insert_note_with_id(self, note):
        """Insert a pre-existing note into the database.

        This is meant to be used to import existing cards from anki.
        """
        assert note.HasField("id")
        assert note.HasField("front")
        assert note.HasField("back")
        assert note.HasField("word")

        if not note.HasField("created_ts"):
            note.created_ts = time.time()

        raw_note = note.SerializeToString()
        self.conn.execute(
            "INSERT INTO notes (id, word, note) VALUES (?, ?, ?)",
            (note.id, note.word, raw_note),
        )
        self.conn.commit()

        return note.id

    def insert_note(self, note):
        """Insert a new note into the database.

        The note should have front and back filled in. The id must not be set,
        and will be assigned in this function.

        Returns the newly created id of the note.
        """
        assert not note.HasField("id")
        note.id = random.randint(0, (1 << 63) - 1)
        return self.insert_note_with_id(note)

    def update_note(self, note):
        """Update a note in the database.

        Replaces the contents of the data for note.id with 'note'. If no note
        exists with that id, raises a KeyError. Note that this assumes that note.word
        does not change, however it does not verify this.
        """
        assert note.HasField("id")
        assert note.HasField("created_ts")
        assert note.HasField("front")
        assert note.HasField("back")

        note.last_edited_ts = time.time()

        # First, check if this note even exists.
        result = self.conn.execute(
            "SELECT EXISTS(SELECT * FROM notes WHERE id=?)", (note.id,)
        )
        exists = result.fetchone()[0]
        if not exists:
            raise KeyError("No note found with id " + str(note.id))

        raw_note = note.SerializeToString()
        self.conn.execute("UPDATE notes SET note = ? WHERE id = ?", (raw_note, note.id))
        self.conn.commit()

    def delete_note(self, note_id):
        """Delete a note from the database."""
        self.conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()

    def find_notes(self, word):
        result = self.conn.execute("SELECT note FROM notes WHERE word = ?", (word,))
        return [note_pb2.Note.FromString(row[0]) for row in result]

    def word_to_count(self):
        """Returns a dictionary mapping word -> number of notes."""
        result = self.conn.execute("SELECT word, COUNT(*) FROM notes GROUP BY word")
        return {row[0]: row[1] for row in result}

    def export_to_csv(self, path):
        num_notes = 0
        with open(path, "w") as f:
            writer = csv.writer(f, delimiter=";", quotechar='"')
            result = self.conn.execute("SELECT note FROM NOTES")
            for row in result:
                note = note_pb2.Note.FromString(row[0])
                fields = [
                    note.id,
                    note.front,
                    "",  # Front picture
                    note.hint,
                    note.word,
                    note.back,
                    note.extra_info,
                    "",  # Two cards?
                ]
                writer.writerow(fields)
                num_notes += 1
        return num_notes
