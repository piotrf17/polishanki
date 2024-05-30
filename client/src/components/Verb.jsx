import { Link } from "react-router-dom";

const Verb = ({ word, verbConjugation }) => {
  const formLink = (form) => {
    return <Link to={`/words/${word}/${form}`}>{form}</Link>;
  };

  const addTenseForms = (forms) => {
    const formAndSpan = [];
    let span = 1;
    let lastForm = forms[0];
    for (let i = 1; i < forms.length; ++i) {
      if (forms[i] == lastForm) {
        span += 1;
      } else {
        formAndSpan.push([lastForm, span]);
        span = 1;
        lastForm = forms[i];
      }
    }
    formAndSpan.push([lastForm, span]);
    return (
      <>
        {formAndSpan.map(([form, span], ix) => (
          <td colSpan={span} key={ix}>
            {formLink(form)}
          </td>
        ))}
      </>
    );
  };

  const addTense = (name, tense) => {
    const hasImpersonal = "impersonal" in tense;
    const rowSpan = hasImpersonal ? "4" : "3";
    return (
      <>
        <tr>
          <th rowSpan={rowSpan}>{name}</th>
          <th>
            1<sup>st</sup>
          </th>
          {addTenseForms(tense.first)}
        </tr>
        <tr>
          <th>
            2<sup>nd</sup>
          </th>
          {addTenseForms(tense.second)}
        </tr>
        <tr>
          <th>
            3<sup>rd</sup>
          </th>
          {addTenseForms(tense.third)}
        </tr>
        {hasImpersonal && (
          <tr>
            <th>impersonal</th>
            {addTenseForms(tense.impersonal)}
          </tr>
        )}
      </>
    );
  };

  return (
    <>
      <h2>Verb</h2>
      <table className="verb-inflection-table">
        <tbody>
          <tr className="header">
            <th rowSpan="2"></th>
            <th rowSpan="2">person</th>
            <th colSpan="3">singular</th>
            <th colSpan="2">plural</th>
          </tr>
          <tr className="header">
            <th>masculine</th>
            <th>feminine</th>
            <th>neuter</th>
            <th>virile</th>
            <th>nonvirile</th>
          </tr>
          <tr>
            <th colSpan="2">infinitive</th>
            <td colSpan="5">{formLink(word)}</td>
          </tr>
          {"present" in verbConjugation &&
            addTense("present tense", verbConjugation.present)}
          {"past" in verbConjugation &&
            addTense("past tense", verbConjugation.past)}
          {"future" in verbConjugation &&
            addTense("future tense", verbConjugation.future)}
          {"conditional" in verbConjugation &&
            addTense("conditional", verbConjugation.conditional)}
          {"imperative" in verbConjugation &&
            addTense("imperative", verbConjugation.imperative)}
          {"activeAdjectivalParticiple" in verbConjugation && (
            <tr>
              <th colSpan="2">active adjectival participle</th>
              {addTenseForms(verbConjugation.activeAdjectivalParticiple)}
            </tr>
          )}
          {"contemporaryAdverbialParticiple" in verbConjugation && (
            <tr>
              <th colSpan="2">contemporary adverbial participle</th>
              {addTenseForms(verbConjugation.contemporaryAdverbialParticiple)}
            </tr>
          )}
          {"anteriorAdverbialParticiple" in verbConjugation && (
            <tr>
              <th colSpan="2">anterior adverbial participle</th>
              {addTenseForms(verbConjugation.anteriorAdverbialParticiple)}
            </tr>
          )}
          {"verbalNoun" in verbConjugation && (
            <tr>
              <th colSpan="2">verbal noun</th>
              {addTenseForms(verbConjugation.verbalNoun)}
            </tr>
          )}
        </tbody>
      </table>
    </>
  );
};

export default Verb;
