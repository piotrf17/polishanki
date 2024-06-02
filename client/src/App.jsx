import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import axios from "axios";

import Notification from "./components/Notification";
import Word from "./components/Word";
import WordForm from "./components/WordForm";
import WordList from "./components/WordList";

const App = () => {
  const [errorMessage, setErrorMessage] = useState(null);

  const padding = {
    padding: 5,
  };

  const handleExport = () => {
    axios
      .get("http://localhost:5000/api/export_to_csv")
      .then((response) => {
        const numNotes = response.data.noteCount;
        setErrorMessage(`exported ${numNotes} notes`);
        setTimeout(() => {
          setErrorMessage(null);
        }, 5000);
      })
      .catch((error) => {
        const serverError =
          "response" in error ? error.response.data.error : error.message;
        setErrorMessage("failed export notes: " + serverError);
      });
  };

  return (
    <Router>
      <Notification message={errorMessage} setErrorMessage={setErrorMessage} />
      <div>
        <Link style={padding} to="/">
          wordlist
        </Link>
        <a href="#" onClick={handleExport}>
          export
        </a>
      </div>
      <Routes>
        <Route path="/" element={<WordList />} />
        <Route path="/:page/:query?" element={<WordList />} />
        <Route
          path="/words/:word"
          element={<Word setErrorMessage={setErrorMessage} />}
        />
        <Route path="/words/:word/:form" element={<WordForm />} />
      </Routes>
    </Router>
  );
};

export default App;
