import Definition from "./Definition";
import { adjectiveDeclensionRow, nounDeclensionRow } from "./wordUtils";

const Pronoun = ({ word, meaning }) => {
  const declensionRow = nounDeclensionRow.bind(null, word, meaning.noun);
  const adjDeclensionRow = adjectiveDeclensionRow.bind(
    null,
    word,
    meaning.adjective
  );
  return (
    <>
      <h2>Pronoun</h2>
      <Definition definitions={meaning.definition} />
      {"noun" in meaning && (
        <table className="noun-inflection-table">
          <tbody>
            <tr className="header">
              <th></th>
              {"singular" in meaning.noun && <th>singular</th>}
              {"plural" in meaning.noun && <th>plural</th>}
            </tr>
            {declensionRow("nominative")}
            {declensionRow("genitive")}
            {declensionRow("dative")}
            {declensionRow("accusative")}
            {declensionRow("instrumental")}
            {declensionRow("locative")}
            {declensionRow("vocative")}
          </tbody>
        </table>
      )}
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
            {adjDeclensionRow("nominative")}
            {adjDeclensionRow("genitive")}
            {adjDeclensionRow("dative")}
            {adjDeclensionRow("accusative")}
            {adjDeclensionRow("instrumental")}
            {adjDeclensionRow("locative")}
          </tbody>
        </table>
      )}
    </>
  );
};

export default Pronoun;
