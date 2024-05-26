import { useState, useEffect } from "react";
import axios from "axios";

import Note from "./Note";

const NoteList = ({ word, noteFilter = (n) => true }) => {
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/notes_for_word/${word}`)
      .then((response) => {
        setNotes(
          response.data
            .map((n) => ({ data: n, editing: false }))
            // Sort to show most recent cards first.
            .sort((a, b) => b.data.createdTs - a.data.createdTs)
            .filter(noteFilter)
        );
      });
  }, []);

  const addNote = () => {
    // Only allow 1 new note at a time.
    if (notes.length > 1 && notes[0].data.id == 0) {
      alert("only one new note at a time");
      return;
    }
    let newNote = {
      data: {
        id: 0,
        createdTs: Date.now() / 1000.0,
        word: word,
      },
      editing: true,
    };
    setNotes([newNote].concat(notes));
  };

  // TODO(piotrf): should we verify that changedData still passes noteFilter?
  const updateData = (changedData) => {
    const id = changedData.id;
    if (id == 0) {
      // If this is a new note, post it to the server and update the ID.
      delete changedData.id;
      axios
        .post("http://localhost:5000/api/notes", changedData)
        .then((response) => {
          const newNote = {
            data: { ...changedData, id: response.data.id },
            editing: false,
          };
          setNotes([newNote].concat(notes.slice(1)));
        });
    } else {
      // Otherwise, just update the data.
      const url = `http://localhost:5000/api/notes/${id}`;
      axios.put(url, changedData).then((response) => {
        setNotes(
          notes.map((n) =>
            n.data.id == id ? { data: changedData, editing: false } : n
          )
        );
      });
    }
  };

  const setEditing = (id, editing) => {
    // If we cancel a pending new note, remove it from the list.
    if (id == 0) {
      setNotes(notes.slice(1));
    } else {
      setNotes(
        notes.map((n) => (n.data.id == id ? { ...n, editing: editing } : n))
      );
    }
  };

  const handleDelete = (id) => {
    if (confirm("Really delete?")) {
      const url = `http://localhost:5000/api/notes/${id}`;
      axios.delete(url).then((response) => {
        setNotes(notes.filter((n) => n.data.id != id));
      });
    }
  };

  return (
    <div>
      <h2>Notes ({notes.length})</h2>
      <div>
        <button onClick={addNote}>Add a new note</button>
      </div>
      {notes.map((n) => (
        <Note
          key={n.data.id}
          data={n.data}
          editing={n.editing}
          updateData={updateData}
          setEditing={setEditing.bind(null, n.data.id)}
          handleDelete={handleDelete.bind(null, n.data.id)}
        />
      ))}
    </div>
  );
};

export default NoteList;
