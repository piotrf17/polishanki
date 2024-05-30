import { useState, useEffect } from "react";
import axios from "axios";

import Example from "./Example";

const ExampleList = ({ word, addExample }) => {
  const [examples, setExamples] = useState([]);
  const [page, setPage] = useState(0);
  const EXAMPLES_PER_PAGE = 20;

  useEffect(() => {
    axios.get(`http://localhost:5000/api/examples/${word}`).then((response) => {
      setExamples(response.data.examples);
    });
  }, []);

  const prevPage = () => {
    setPage(page - 1);
  };
  // TODO(piotrf): handle the true last page
  const nextPage = () => {
    const numPages = Math.ceil(examples.length / EXAMPLES_PER_PAGE);
    if (page < numPages - 1) {
      setPage(page + 1);
    } else {
      axios
        .get(`http://localhost:5000/api/examples/${word}/scrape_next_page`)
        .then((response) => {
          const newNumExamples = response.data.examples.length;
          if (newNumExamples > examples.length) {
            setExamples(response.data.examples);
            setPage(page + 1);
          }
        });
    }
  };

  const firstExampleIx = page * EXAMPLES_PER_PAGE;
  const lastExampleIx = (page + 1) * EXAMPLES_PER_PAGE;

  return (
    <>
      <h2>Examples</h2>
      <a
        href={"https://context.reverso.net/translation/polish-english/" + word}
      >
        [reverso]
      </a>
      <div>
        {page > 0 && (
          <a href="#" onClick={prevPage}>
            [prev]
          </a>
        )}
        {page == 0 && <span>[prev]</span>}
        &nbsp;
        <span>
          examples {firstExampleIx + 1} through {lastExampleIx}
        </span>
        &nbsp;
        <a href="#" onClick={nextPage}>
          [next]
        </a>
      </div>
      {examples.slice(firstExampleIx, lastExampleIx).map((example, ix) => (
        <div key={ix} className="example-holder">
          <Example word={word} example={example} />
          <button onClick={addExample.bind(null, example)}>Add</button>
        </div>
      ))}
    </>
  );
};

export default ExampleList;
