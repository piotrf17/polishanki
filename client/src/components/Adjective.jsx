import { Link } from "react-router-dom";

import Definition from "./Definition";

const Adjective = ({ word, meaning }) => {
  const adjectiveDeclension = meaning.adjective;

  const formLink = (form) => {
    return <Link to={`/words/${word}/${form}`}>{form}</Link>;
  };

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
          {formLink(adjectiveDeclension.masculineAnimate[adjCase])}
        </td>
        {!singularSame && (
          <td>{formLink(adjectiveDeclension.masculineInanimate[adjCase])}</td>
        )}
        <td>{formLink(adjectiveDeclension.feminine[adjCase])}</td>
        <td>{formLink(adjectiveDeclension.neuter[adjCase])}</td>
        <td colSpan={pluralSame ? "2" : "1"}>
          {formLink(adjectiveDeclension.pluralVirile[adjCase])}
        </td>
        {!pluralSame && (
          <td>{formLink(adjectiveDeclension.pluralNonvirile[adjCase])}</td>
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
