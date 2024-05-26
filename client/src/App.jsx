import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Word from "./Word";
import WordForm from "./WordForm";
import WordList from "./WordList";

const App = () => {
  const padding = {
    padding: 5,
  };

  return (
    <Router>
      <div>
        <Link style={padding} to="/">
          wordlist
        </Link>
      </div>
      <Routes>
        <Route path="/" element={<WordList />} />
        <Route path="/:page/:query?" element={<WordList />} />
        <Route path="/words/:word" element={<Word />} />
        <Route path="/words/:word/:form" element={<WordForm />} />
      </Routes>
    </Router>
  );
};

export default App;
