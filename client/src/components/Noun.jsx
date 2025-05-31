import Definition from "./Definition";
import { nounDeclensionRow } from "./wordUtils";

const Noun = ({ word, meaning }) => {
  const declensionRow = nounDeclensionRow.bind(null, word, meaning.noun);
  return (
    <>
      <h2>Noun</h2>
      <div className="gender">
        <span>
          {meaning.gender == "kMasculinePersonal" && "masculine personal"}
          {meaning.gender == "kMasculineAnimate" && "masculine animate"}
          {meaning.gender == "kMasculineInanimate" && "masculine inanimate"}
          {meaning.gender == "kFeminine" && "feminine"}
          {meaning.gender == "kNeuter" && "neuter"}
        </span>
      </div>
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
    </>
  );
};

export default Noun;
