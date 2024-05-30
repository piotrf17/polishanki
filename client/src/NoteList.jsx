import { useState, useEffect } from "react";
import axios from "axios";

import Note from "./Note";
import NoteService from "./services/notes";

const NoteList = ({ word, noteFilter = (n) => true }) => {
  const [notes, setNotes] = useState([]);
  const noteService = new NoteService(notes, setNotes, noteFilter);

  useEffect(() => {
    noteService.getNotes(word);
  }, []);

  return (
    <div>
      <h2>Notes ({notes.length})</h2>
      <div>
        <button
          onClick={() => {
            noteService.addNote(word);
          }}
        >
          Add a new note
        </button>
      </div>
      {notes.map((n) => (
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
