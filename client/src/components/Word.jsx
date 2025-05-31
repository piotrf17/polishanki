import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

import Adjective from "./Adjective";
import NoteList from "./NoteList";
import NoteService from "../services/notes";
import Noun from "./Noun";
import Pronoun from "./Pronoun";
import Verb from "./Verb";

const Word = ({ setErrorMessage }) => {
  const word = useParams().word;
  const [wordData, setWordData] = useState(null);
  const noteService = new NoteService();

  useEffect(() => {
    axios
      .get(`http://localhost:5000/api/words/${word}`)
      .then((response) => {
        setWordData(response.data);
      })
      .catch((error) => {
        const serverError = error.response.data.error;
        setErrorMessage("failed to lookup wiktionary data: " + serverError);
      });
  }, []);

  return (
    <>
      <h1>{word}</h1>
      <a href={"https://en.wiktionary.org/wiki/" + word + "#Polish"}>
        [wiktionary]
      </a>
      <a href={"https://pl.wiktionary.org/wiki/" + word + "#Polish"}>
        [wiktionary-pl]
      </a>
      {wordData && (
        <div>
          {wordData.meanings.map((meaning, index) => (
            <div key={index}>
              {meaning.partOfSpeech == "kNoun" && (
                <Noun word={word} meaning={meaning} />
              )}
              {meaning.partOfSpeech == "kVerb" && (
                <Verb word={word} meaning={meaning} />
              )}
              {meaning.partOfSpeech == "kAdjective" && (
                <Adjective word={word} meaning={meaning} />
              )}
              {meaning.partOfSpeech == "kPronoun" && (
                <Pronoun word={word} meaning={meaning} />
              )}
            </div>
          ))}
        </div>
      )}
      <NoteList word={word} noteService={noteService} />
    </>
  );
};

export default Word;
