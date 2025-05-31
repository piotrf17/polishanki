import { Link } from "react-router-dom";

import Definition from "./Definition";
import { adjectiveDeclensionRow } from "./wordUtils";

const Adjective = ({ word, meaning }) => {
  const declensionRow = adjectiveDeclensionRow.bind(
    null,
    word,
    meaning.adjective
  );

  return (
    <>
      <h2>Adjective</h2>
      <Definition definitions={meaning.definition} />
      {"adjective" in meaning && (
        <table className="verb-inflection-table">
          <tbody>
            <tr className="header">
              <th colSpan="5">singular</th>
              <th colSpan="2">plural</th>
            </tr>
            <tr>
              <th></th>
              <th>masculine animate</th>
              <th>masculine inanimate</th>
              <th>feminine</th>
              <th>neuter</th>
              <th>virile</th>
              <th>nonvirile</th>
            </tr>
            {declensionRow("nominative")}
            {declensionRow("genitive")}
            {declensionRow("dative")}
            {declensionRow("accusative")}
            {declensionRow("instrumental")}
            {declensionRow("locative")}
          </tbody>
        </table>
      )}
    </>
  );
};

export default Adjective;
