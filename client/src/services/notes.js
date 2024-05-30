import { useState } from "react";
import axios from "axios";

const baseUrl = "http://localhost:5000/api";

class NoteService {
  constructor(noteFilter = (n) => true) {
    const [notes, setNotes] = useState([]);
    this.notes = notes;
    this.setNotes = setNotes;
    this.noteFilter = noteFilter;
  }

  getNotes(word) {
    axios.get(`${baseUrl}/notes_for_word/${word}`).then((response) => {
      this.setNotes(
        response.data
          .map((n) => ({ data: n, editing: false }))
          // Sort to show most recent cards first.
          .sort((a, b) => b.data.createdTs - a.data.createdTs)
          .filter(this.noteFilter)
      );
    });
  }

  addNote(word, data = {}) {
    // Only allow 1 new note at a time.
    if (this.notes.length > 1 && this.notes[0].data.id == 0) {
      alert("only one new note at a time");
      return;
    }
    let newNote = {
      data: {
        ...data,
        id: 0,
        createdTs: Date.now() / 1000.0,
        word: word,
      },
      editing: true,
    };
    this.setNotes([newNote].concat(this.notes));
  }

  // TODO(piotrf): should we verify that changedData still passes noteFilter?
  updateNoteData(changedData) {
    const id = changedData.id;
    if (id == 0) {
      // If this is a new note, post it to the server and update the ID.
      delete changedData.id;
      axios.post(`${baseUrl}/notes`, changedData).then((response) => {
        const newNote = {
          data: { ...changedData, id: response.data.id },
          editing: false,
        };
        this.setNotes([newNote].concat(this.notes.slice(1)));
      });
    } else {
      // Otherwise, just update the data.
      const url = `${baseUrl}/notes/${id}`;
      axios.put(url, changedData).then((response) => {
        this.setNotes(
          this.notes.map((n) =>
            n.data.id == id ? { data: changedData, editing: false } : n
          )
        );
      });
    }
  }

  setEditing(id, editing) {
    // If we cancel a pending new note, remove it from the list.
    if (id == 0) {
      this.setNotes(this.notes.slice(1));
    } else {
      this.setNotes(
        this.notes.map((n) =>
          n.data.id == id ? { ...n, editing: editing } : n
        )
      );
    }
  }

  deleteNote(id) {
    if (confirm("Really delete?")) {
      const url = `${baseUrl}/notes/${id}`;
      axios.delete(url).then((response) => {
        this.setNotes(this.notes.filter((n) => n.data.id != id));
      });
    }
  }
}

export default NoteService;
