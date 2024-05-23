import { useState, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import axios from "axios";

const WordList = () => {
  const params = useParams();
  const currentPage = "page" in params ? parseInt(params.page) : 1;
  const [allWords, setAllWords] = useState([]);
  const [numPages, setNumPages] = useState(0);
  const WORDS_PER_PAGE = 100;

  useEffect(() => {
    axios.get("http://localhost:5000/api/wordlist").then((response) => {
      setAllWords(response.data);
      setNumPages(Math.ceil(response.data.length / WORDS_PER_PAGE));
    });
  }, []);

  const words = allWords.slice(
    (currentPage - 1) * WORDS_PER_PAGE,
    currentPage * WORDS_PER_PAGE
  );

  return (
    <>
      <h1>Wordlist</h1>
      <div>
        {currentPage > 1 && <Link to={"/" + (currentPage - 1)}>prev</Link>}
        &nbsp;
        <span>
          page {currentPage} of {numPages}
        </span>
        &nbsp;
        {currentPage < numPages && (
          <Link to={"/" + (currentPage + 1)}>next</Link>
        )}
      </div>
      <div>
        <ul>
          {words.slice(0, 100).map((word) => (
            <li key={word}>
              <Link to={"/words/" + word}>{word}</Link>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
};

export default WordList;
