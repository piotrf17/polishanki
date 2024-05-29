import { useState, useEffect } from "react";
import axios from "axios";

import Example from "./Example";

const ExampleList = ({ word }) => {
  const [examples, setExamples] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:5000/api/examples/${word}`).then((response) => {
      setExamples(response.data.examples);
    });
  }, []);

  return (
    <>
      <h2>Examples</h2>
      <a
        href={"https://context.reverso.net/translation/polish-english/" + word}
      >
        [reverso]
      </a>
      {examples.map((example, ix) => (
        <Example key={ix} word={word} example={example} />
      ))}
    </>
  );
};

export default ExampleList;
