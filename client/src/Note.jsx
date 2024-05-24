const Note = ({ data }) => {
  return (
    <div>
      <table>
        <tbody>
          <tr>
            <th>Front</th>
            <td>{data.front}</td>
          </tr>
          <tr>
            <th>Back</th>
            <td>{data.back}</td>
          </tr>
          <tr>
            <th>Hint</th>
            <td>{data.hint}</td>
          </tr>
          <tr>
            <th>Extra Info</th>
            <td>{data.extra_info}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default Note;
