import { Link } from "react-router-dom";

import Definition from "./Definition";
import { formLink } from "./wordUtils";

const shortAspectString = (aspect) => {
  switch (aspect) {
    case "kImperfective":
      return "impf";
    case "kPerfective":
      return "perf";
    case "kBiaspectual":
      return "";
  }
};

const isDefective = (verbConjugation) => {
  const allEqual = (arr) => arr.every((v) => v === arr[0]);
  const checkTense = (tense) => {
    if ("second" in tense) return false;
    return allEqual(tense.first);
  };
  if ("present" in verbConjugation && !checkTense(verbConjugation.present))
    return false;
  if ("past" in verbConjugation && !checkTense(verbConjugation.past))
    return false;
  if ("future" in verbConjugation && !checkTense(verbConjugation.future))
    return false;

  return true;
};

const Verb = ({ word, meaning }) => {
  const verbConjugation = meaning.verb;
  if (verbConjugation === undefined) {
    return (
      <>
        <span>(definition missing conjugation)</span>
      </>
    );
  }
  const makeExtraInfo = (tense) => {
    const aspect = shortAspectString(meaning.aspect);
    return aspect == "" ? tense : aspect + "; " + tense;
  };
  const defective = isDefective(meaning.verb);

  const addTenseForms = (forms, extraInfo) => {
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
            {formLink(word, form, extraInfo)}
          </td>
        ))}
      </>
    );
  };

  const addTense = (name, tense) => {
    const shortName = name.split(" ")[0];
    const extraInfo = makeExtraInfo(shortName);
    const numPersons = Object.keys(tense).length;
    return (
      <>
        <tr>
          <th rowSpan={numPersons}>{name}</th>
          {!defective && (
            <th>
              1<sup>st</sup>
            </th>
          )}
          {addTenseForms(tense.first, extraInfo)}
        </tr>
        {"second" in tense && (
          <tr>
            <th>
              2<sup>nd</sup>
            </th>
            {addTenseForms(tense.second, extraInfo)}
          </tr>
        )}
        {"third" in tense && (
          <tr>
            <th>
              3<sup>rd</sup>
            </th>
            {addTenseForms(tense.third, extraInfo)}
          </tr>
        )}
        {"impersonal" in tense && (
          <tr>
            <th>impersonal</th>
            {addTenseForms(tense.impersonal, extraInfo)}
          </tr>
        )}
      </>
    );
  };

  const makeHeader = () =>
    defective ? (
      <tr className="header">
        <th></th>
        <th>defective</th>
      </tr>
    ) : (
      <>
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
      </>
    );

  return (
    <>
      <h2>Verb</h2>
      <div className="aspect">
        <span>
          {meaning.aspect == "kImperfective" && "imperfective"}
          {meaning.aspect == "kPerfective" && "perfective"}
          {meaning.aspect == "kBiaspectual" && "biaspectual"}
        </span>
      </div>
      <Definition definitions={meaning.definition} />
      {"verb" in meaning && (
        <table className="verb-inflection-table">
          <tbody>
            {makeHeader()}
            <tr>
              <th colSpan={defective ? "1" : "2"}>infinitive</th>
              <td colSpan={defective ? "1" : "5"}>
                {formLink(word, word, makeExtraInfo("infinitive"))}
              </td>
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
                {addTenseForms(
                  verbConjugation.activeAdjectivalParticiple,
                  makeExtraInfo("active adjectival participle")
                )}
              </tr>
            )}
            {"contemporaryAdverbialParticiple" in verbConjugation && (
              <tr>
                <th colSpan="2">contemporary adverbial participle</th>
                {addTenseForms(
                  verbConjugation.contemporaryAdverbialParticiple,
                  makeExtraInfo("contemporary adverbial participle")
                )}
              </tr>
            )}
            {"anteriorAdverbialParticiple" in verbConjugation && (
              <tr>
                <th colSpan="2">anterior adverbial participle</th>
                {addTenseForms(
                  verbConjugation.anteriorAdverbialParticiple,
                  makeExtraInfo("anterior adverbial participle")
                )}
              </tr>
            )}
            {"verbalNoun" in verbConjugation && (
              <tr>
                <th colSpan="2">verbal noun</th>
                {addTenseForms(
                  verbConjugation.verbalNoun,
                  makeExtraInfo("verbal noun")
                )}
              </tr>
            )}
          </tbody>
        </table>
      )}
    </>
  );
};

export default Verb;
