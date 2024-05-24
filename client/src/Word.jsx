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
    axios.get("http://localhost:5000/api/words/" + word).then((response) => {
      setScrapeTime(response.data.scrape_time);
      setWordData(response.data.word_data);
    });
  }, []);

  useEffect(() => {
    axios.get("http://localhost:5000/api/notes/" + word).then((response) => {
      setNotes(response.data);
    });
  }, []);

  return (
    <>
      <h1>{word}</h1>
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
        <h2>Notes</h2>
        {notes.map((note) => (
          <Note key={note.id} data={note} />
        ))}
      </div>
    </>
  );
};

export default Word;
