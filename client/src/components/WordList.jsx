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
  const [matchAll, setMatchAll] = useState(true);
  const [matchNouns, setMatchNouns] = useState(true);
  const [matchVerbs, setMatchVerbs] = useState(true);
  const [matchAdjectives, setMatchAdjectives] = useState(true);
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

  const matchesPosFilter = (wordData) => {
    if (matchAll) return true;
    if (matchNouns && wordData.has_noun) return true;
    if (matchVerbs && wordData.has_verb) return true;
    if (matchAdjectives && wordData.has_adjective) return true;
    return false;
  };

  const matchingWords = allWords.filter((wordData) => {
    // First, match on parts of speech.
    if (!matchesPosFilter(wordData)) {
      return false;
    }

    // Next, match on query.
    const word = wordData.word;
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
        <span>
          <input
            type="checkbox"
            defaultChecked={matchAll}
            onChange={(e) => {
              setMatchAll(e.target.checked);
            }}
          />{" "}
          All
          <input
            type="checkbox"
            disabled={matchAll}
            defaultChecked={matchNouns}
            onChange={(e) => {
              setMatchNouns(e.target.checked);
            }}
          />{" "}
          Nouns
          <input
            type="checkbox"
            disabled={matchAll}
            defaultChecked={matchVerbs}
            onChange={(e) => {
              setMatchVerbs(e.target.checked);
            }}
          />{" "}
          Verbs
          <input
            type="checkbox"
            disabled={matchAll}
            defaultChecked={matchAdjectives}
            onChange={(e) => {
              setMatchAdjectives(e.target.checked);
            }}
          />{" "}
          Adjectives
        </span>
      </div>
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
        <table>
          <tbody>
            {words.map((wordData) => (
              <tr key={wordData.ix}>
                <td>{wordData.ix + 1}. </td>
                <td>
                  <Link to={"/words/" + wordData.word}>{wordData.word}</Link>
                </td>
                <td>
                  {wordData.note_count > 0 && wordData.note_count}
                  {wordData.note_count == 1 && " note"}
                  {wordData.note_count > 1 && " notes"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default WordList;
