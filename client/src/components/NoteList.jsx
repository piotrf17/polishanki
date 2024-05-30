import { useState, useEffect } from "react";
import axios from "axios";

import Note from "./Note";

const NoteList = ({ word, noteService }) => {
  useEffect(() => {
    noteService.getNotes(word);
  }, []);

  return (
    <div>
      <h2>Notes ({noteService.notes.length})</h2>
      <div>
        <button
          onClick={() => {
            noteService.addNote(word);
          }}
        >
          Add a new note
        </button>
      </div>
      {noteService.notes.map((n) => (
        <Note
          key={n.data.id}
          data={n.data}
          editing={n.editing}
          updateData={(changedData) => {
            noteService.updateNoteData(changedData);
          }}
          setEditing={(editing) => {
            noteService.setEditing(n.data.id, editing);
          }}
          handleDelete={() => {
            noteService.deleteNote(n.data.id);
          }}
        />
      ))}
    </div>
  );
};

export default NoteList;
