import { Link, useParams } from "react-router-dom";

import ExampleList from "./ExampleList";
import NoteList from "./NoteList";

const wordsInBlank = (front, back) => {
  let startIx = 0;
  for (; startIx < Math.min(front.length, back.length); ++startIx) {
    if (front[startIx] != back[startIx]) break;
  }
  let endIx = 0; // Relative from end of string.
  for (; endIx < Math.min(front.length, back.length); ++endIx) {
    if (front[front.length - 1 - endIx] != back[back.length - 1 - endIx]) break;
  }

  return back.substr(startIx, back.length - startIx - endIx).split(" ");
};

const WordForm = () => {
  const { word: word, form: form } = useParams();

  const filterToForm = (n) => {
    const words = wordsInBlank(n.data.front, n.data.back);
    return words.includes(form);
  };

  return (
    <>
      <h1>
        <Link to={`/words/${word}`}>{word}</Link> -- {form}
      </h1>
      <ExampleList word={word} />
      <NoteList word={word} noteFilter={filterToForm} />
    </>
  );
};

export default WordForm;
