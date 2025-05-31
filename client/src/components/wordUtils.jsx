import { Link } from "react-router-dom";

export const shortCaseString = (nounCase) => {
  switch (nounCase) {
    case "nominative":
      return "nom";
    case "genitive":
      return "gen";
    case "dative":
      return "dat";
    case "accusative":
      return "acc";
    case "instrumental":
      return "instr";
    case "locative":
      return "loc";
    case "vocative":
      return "voc";
  }
};

export const formLink = (word, form, extraInfo) => {
  const forms = form.split("/").map((form) => form.trim());
  const query = extraInfo ? `?extra_info=${encodeURIComponent(extraInfo)}` : "";
  const url = `/words/${word}/${form}` + query;
  return (
    <>
      {forms.map((form, ix) => (
        <Link key={ix} to={url}>
          {ix > 0 ? " / " : ""}
          {form}
        </Link>
      ))}
    </>
  );
};

export const nounDeclensionRow = (word, nounDeclension, nounCase) => {
  const hasSingular = "singular" in nounDeclension;
  const hasPlural = "plural" in nounDeclension;
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

export const adjectiveDeclensionRow = (word, adjectiveDeclension, adjCase) => {
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
