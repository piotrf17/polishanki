import { Link } from "react-router-dom";

const Noun = ({ word, nounDeclension }) => {
  const formLink = (form) => {
    return <Link to={`/words/${word}/${form}`}>{form}</Link>;
  };

  return (
    <>
      <h2>Noun</h2>
      <table>
        <tbody>
          <tr>
            <th></th>
            <th>singular</th>
            <th>plural</th>
          </tr>
          <tr>
            <th>nominative</th>
            <td>{formLink(nounDeclension.singular.nominative)}</td>
            <td>{formLink(nounDeclension.plural.nominative)}</td>
          </tr>
        </tbody>
      </table>
    </>
  );
};

export default Noun;
