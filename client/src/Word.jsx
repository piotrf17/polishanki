import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const Word = () => {
  const word = useParams().word;
  const [wordData, setWordData] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:5000/api/words/" + word).then((response) => {
      setWordData(response.data);
    });
  }, []);

  return (
    <>
      <h2>{word}</h2>
      {wordData && (
        <div>
          <p>nominative: {wordData["inflection"]["nominative"]}</p>
          <p>genitive: {wordData["inflection"]["genitive"]}</p>
        </div>
      )}
    </>
  );
};

export default Word;
