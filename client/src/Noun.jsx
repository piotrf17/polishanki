const Noun = ({ nounDeclension }) => {
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
            <td>{nounDeclension.singular.nominative}</td>
            <td>{nounDeclension.plural.nominative}</td>
          </tr>
        </tbody>
      </table>
    </>
  );
};

export default Noun;
