import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Notification from "./components/Notification";
import Word from "./components/Word";
import WordForm from "./components/WordForm";
import WordList from "./components/WordList";

const App = () => {
  const [errorMessage, setErrorMessage] = useState(null);

  const padding = {
    padding: 5,
  };

  return (
    <Router>
      <Notification message={errorMessage} />
      <div>
        <Link style={padding} to="/">
          wordlist
        </Link>
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
