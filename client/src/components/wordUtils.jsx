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
