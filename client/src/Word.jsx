import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

import Note from "./Note";
import Noun from "./Noun";

const Word = () => {
  const word = useParams().word;
  const [scrapeTime, setScrapeTime] = useState(0.0);
  const [wordData, setWordData] = useState(null);
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:5000/api/words/${word}`).then((response) => {
      setScrapeTime(response.data.scrape_time);
      setWordData(response.data.word_data);
    });
  }, []);

  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/notes_for_word/${word}`)
      .then((response) => {
        setNotes(
          response.data
            .map((n) => ({ data: n, editing: false }))
            // Sort to show most recent cards first.
            .sort((a, b) => b.data.createdTs - a.data.createdTs)
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
    <>
      <h1>{word}</h1>
      <a href={"https://en.wiktionary.org/wiki/" + word + "#Polish"}>
        [wiktionary]
      </a>
      {wordData && (
        <div>
          {wordData.meanings.map((meaning, index) => (
            <div key={index}>
              {meaning.partOfSpeech == "kNoun" && (
                <Noun nounDeclension={meaning.noun} />
              )}
              {meaning.partOfSpeech == "kVerb" && <h2>Verb</h2>}
              {meaning.partOfSpeech == "kAdjective" && <h2>Adjective</h2>}
            </div>
          ))}
        </div>
      )}
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
    </>
  );
};

export default Word;
