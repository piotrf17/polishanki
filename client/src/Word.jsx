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
        setNotes(response.data);
      });
  }, []);

  const updateNote = (changedNote) => {
    setNotes(notes.map((n) => (n.id == changedNote.id ? changedNote : n)));
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
        {notes.map((note) => (
          <Note key={note.id} data={note} updateData={updateNote} />
        ))}
      </div>
    </>
  );
};

export default Word;
