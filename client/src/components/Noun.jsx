import Definition from "./Definition";
import { shortCaseString, formLink } from "./wordUtils";

const Noun = ({ word, meaning }) => {
  const nounDeclension = meaning.noun;
  const hasSingular = "singular" in nounDeclension;
  const hasPlural = "plural" in nounDeclension;

  const declensionRow = (nounCase) => {
    return (
      <tr>
        <th>{nounCase}</th>
        {hasSingular && (
          <td>
            {formLink(
              word,
              nounDeclension.singular[nounCase],
              shortCaseString(nounCase)
            )}
          </td>
        )}
        {hasPlural && (
          <td>
            {formLink(
              word,
              nounDeclension.plural[nounCase],
              shortCaseString(nounCase) + " pl"
            )}
          </td>
        )}
      </tr>
    );
  };

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
              {hasSingular && <th>singular</th>}
              {hasPlural && <th>plural</th>}
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
