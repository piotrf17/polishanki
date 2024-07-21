import { Link } from "react-router-dom";

import Definition from "./Definition";
import { shortCaseString, formLink } from "./wordUtils";

const Adjective = ({ word, meaning }) => {
  const adjectiveDeclension = meaning.adjective;

  const declensionRow = (adjCase) => {
    const singularSame =
      adjectiveDeclension.masculineAnimate[adjCase] ==
      adjectiveDeclension.masculineInanimate[adjCase];
    const pluralSame =
      adjectiveDeclension.pluralVirile[adjCase] ==
      adjectiveDeclension.pluralNonvirile[adjCase];
    return (
      <tr>
        <th>{adjCase}</th>
        <td colSpan={singularSame ? "2" : "1"}>
          {formLink(
            word,
            adjectiveDeclension.masculineAnimate[adjCase],
            shortCaseString(adjCase) + (singularSame ? " m" : " men")
          )}
        </td>
        {!singularSame && (
          <td>
            {formLink(
              word,
              adjectiveDeclension.masculineInanimate[adjCase],
              shortCaseString(adjCase) + " m"
            )}
          </td>
        )}
        <td>
          {formLink(
            word,
            adjectiveDeclension.feminine[adjCase],
            shortCaseString(adjCase) + " f"
          )}
        </td>
        <td>
          {formLink(
            word,
            adjectiveDeclension.neuter[adjCase],
            shortCaseString(adjCase) + " n"
          )}
        </td>
        <td colSpan={pluralSame ? "2" : "1"}>
          {formLink(
            word,
            adjectiveDeclension.pluralVirile[adjCase],
            shortCaseString(adjCase) + (pluralSame ? " pl" : " pl virile")
          )}
        </td>
        {!pluralSame && (
          <td>
            {formLink(
              word,
              adjectiveDeclension.pluralNonvirile[adjCase],
              shortCaseString(adjCase) + " pl nonvirile"
            )}
          </td>
        )}
      </tr>
    );
  };

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
