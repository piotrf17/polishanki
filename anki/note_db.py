import random
import sqlite3
import time

SCHEMA = """
DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
  id INTEGER PRIMARY KEY,
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

        if not note.HasField("created_ts"):
            note.created_ts = time.time()

        raw_note = note.SerializeToString()
        self.conn.execute(
            "INSERT INTO notes (id, note) VALUES (?, ?)", (note.id, raw_note)
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
        self.insert_note_with_id(note)

    def update_note(self, note):
        """Update a note in the database.

        Replaces the contents of the data for note.id with 'note'. If no note
        exists with that id, raises a KeyError.
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
