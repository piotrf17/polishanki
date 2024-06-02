import { Link } from "react-router-dom";

const Noun = ({ word, nounDeclension }) => {
  // TODO(piotrf): refactor to library and use with Verb and Adjective.
  const formLink = (form) => {
    const forms = form.split("/").map((form) => form.trim());
    return (
      <>
        {forms.map((form, ix) => (
          <Link key={ix} to={`/words/${word}/${form}`}>
            {ix > 0 ? " / " : ""}
            {form}
          </Link>
        ))}
      </>
    );
  };

  const hasSingular = "singular" in nounDeclension;
  const hasPlural = "plural" in nounDeclension;

  const declensionRow = (nounCase) => {
    return (
      <tr>
        <th>{nounCase}</th>
        {hasSingular && <td>{formLink(nounDeclension.singular[nounCase])}</td>}
        {hasPlural && <td>{formLink(nounDeclension.plural[nounCase])}</td>}
      </tr>
    );
  };

  return (
    <>
      <h2>Noun</h2>
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
    </>
  );
};

export default Noun;
