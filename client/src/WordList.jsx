import { useState, useEffect } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import axios from "axios";

const getUrl = (page, query) => {
  if (query == "") {
    return "/" + page;
  }
  return "/" + page + "/" + query;
};

const WordList = () => {
  const params = useParams();
  const currentPage = "page" in params ? parseInt(params.page) : 1;
  const query = ("query" in params ? params.query : "").toLowerCase();
  const [allWords, setAllWords] = useState([]);
  const WORDS_PER_PAGE = 100;
  const navigate = useNavigate();

  useEffect(() => {
    axios.get("http://localhost:5000/api/wordlist").then((response) => {
      setAllWords(response.data);
    });
  }, []);

  const handleSearch = (e) => {
    const query = e.target.value;
    // Always navigate to page 1 when searching.
    navigate(getUrl(1, query));
  };

  const matchingWords = allWords.filter((word) => {
    if (query == "") {
      return true;
    }
    // Match directly (including diacritics).
    if (word.indexOf(query) != -1) {
      return true;
    }
    // Also try matching without diacritics.
    const normalizedWord = word
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
    return normalizedWord.indexOf(query) != -1;
  });

  const numPages = Math.ceil(matchingWords.length / WORDS_PER_PAGE);

  const words = matchingWords.slice(
    (currentPage - 1) * WORDS_PER_PAGE,
    currentPage * WORDS_PER_PAGE
  );

  return (
    <>
      <h1>Wordlist</h1>
      <div>
        {currentPage > 1 && (
          <Link to={getUrl(currentPage - 1, query)}>prev</Link>
        )}
        &nbsp;
        <span>
          page {currentPage} of {numPages}
        </span>
        &nbsp;
        {currentPage < numPages && (
          <Link to={getUrl(currentPage + 1, query)}>next</Link>
        )}
      </div>
      <div>
        <span>Search: </span>
        <input onChange={handleSearch} value={query} />
      </div>
      <div>
        <ul>
          {words.map((word) => (
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
