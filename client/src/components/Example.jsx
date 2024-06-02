import { useState } from "react";

const boldWord = (word, example) => {
  const startIx = example.toLowerCase().indexOf(word);
  if (startIx == -1) return example;
  return (
    <span>
      {example.substring(0, startIx)}
      <b>{example.substring(startIx, startIx + word.length)}</b>
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
      {selected && (
        <p className="source">
          <b>Source:</b> {example.source}
        </p>
      )}
    </div>
  );
};

export default Example;
