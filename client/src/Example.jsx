import { useState } from "react";

const boldWord = (word, example) => {
  const startIx = example.indexOf(word);
  return (
    <span>
      {example.substring(0, startIx)}
      <b>{word}</b>
      {example.substring(startIx + word.length)}
    </span>
  );
};

const Example = ({ word, example }) => {
  const [selected, setSelected] = useState(false);

  return (
    <div
      className={selected ? "example exampleSelected" : "example"}
      onClick={() => {
        setSelected(!selected);
      }}
    >
      <p>{boldWord(word, example.polish)}</p>
      {selected && <p>{example.english}</p>}
      {selected && <p>Source: {example.source}</p>}
    </div>
  );
};

export default Example;
