import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

import NoteList from "./NoteList";
import NoteService from "../services/notes";
import Noun from "./Noun";
import Verb from "./Verb";

const Word = () => {
  const word = useParams().word;
  const [scrapeTime, setScrapeTime] = useState(0.0);
  const [wordData, setWordData] = useState(null);
  const noteService = new NoteService();

  useEffect(() => {
    axios.get(`http://localhost:5000/api/words/${word}`).then((response) => {
      setScrapeTime(response.data.scrape_time);
      setWordData(response.data.word_data);
    });
  }, []);

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
                <Noun word={word} nounDeclension={meaning.noun} />
              )}
              {meaning.partOfSpeech == "kVerb" && (
                <Verb word={word} verbConjugation={meaning.verb} />
              )}
              {meaning.partOfSpeech == "kAdjective" && <h2>Adjective</h2>}
            </div>
          ))}
        </div>
      )}
      <NoteList word={word} noteService={noteService} />
    </>
  );
};

export default Word;
