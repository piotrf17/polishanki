import { useState } from "react";

const timestampToDate = (unixSeconds) => {
  if (typeof unixSeconds == "undefined") return " never";
  const date = new Date(unixSeconds * 1000);
  return date.toLocaleString();
};

const Note = ({ data }) => {
  const [editing, setEditing] = useState(false);

  const handleDoubleClick = () => {
    // If already editing, do nothing.
    if (editing) return;
    setEditing(true);
  };

  const handleCancelEdit = () => {
    setEditing(false);
  };

  return (
    <div
      className="note"
      onDoubleClick={handleDoubleClick}
      data-editing={editing}
    >
      <table>
        <tbody>
          <tr>
            <th>Front</th>
            <td>{editing ? <input value={data.front} /> : data.front}</td>
          </tr>
          <tr>
            <th>Back</th>
            <td>{editing ? <input value={data.back} /> : data.back}</td>
          </tr>
          <tr>
            <th>Hint</th>
            <td>{editing ? <input value={data.hint} /> : data.hint}</td>
          </tr>
          <tr>
            <th>Extra Info</th>
            <td>
              {editing ? <input value={data.extraInfo} /> : data.extraInfo}
            </td>
          </tr>
        </tbody>
      </table>
      {editing && (
        <div>
          <div className="buttons">
            <button>Save</button>
            &nbsp;&nbsp;&nbsp;
            <button onClick={handleCancelEdit}>Cancel</button>
          </div>
          <span className="timeInfo">
            <b>Created:</b> {timestampToDate(data.createdTs)}{" "}
            <b>Last edited:</b>
            {timestampToDate(data.lastEditedTs)}
          </span>
        </div>
      )}
    </div>
  );
};

export default Note;
