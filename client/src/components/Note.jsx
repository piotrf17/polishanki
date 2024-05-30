const timestampToDate = (unixSeconds) => {
  if (typeof unixSeconds == "undefined") return " never";
  const date = new Date(unixSeconds * 1000);
  return date.toLocaleString();
};

const Note = ({ data, editing, updateData, setEditing, handleDelete }) => {
  const handleDoubleClick = () => {
    // If already editing, do nothing.
    if (editing) return;
    setEditing(true);
  };

  const handleSave = (e) => {
    // Prevent the browser from reloading the page
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const formJson = Object.fromEntries(formData.entries());

    const changedData = {
      ...data,
      front: formJson.front,
      back: formJson.back,
      hint: formJson.hint,
      extraInfo: formJson.extraInfo,
    };

    // If nothing has changed, just reset editing.
    if (
      data.front == changedData.front &&
      data.back == changedData.back &&
      data.hint == changedData.hint &&
      data.extraInfo == changedData.extraInfo
    ) {
      setEditing(false);
    }

    updateData(changedData);
  };

  const handleCancel = () => {
    setEditing(false);
  };

  return (
    <div
      className="note"
      onDoubleClick={handleDoubleClick}
      data-editing={editing}
    >
      {!editing && (
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
              <td>{data.extraInfo}</td>
            </tr>
          </tbody>
        </table>
      )}
      {editing && (
        <form method="post" onSubmit={handleSave}>
          <table>
            <tbody>
              <tr>
                <th>Front</th>
                <td>
                  <input name="front" defaultValue={data.front} />
                </td>
              </tr>
              <tr>
                <th>Back</th>
                <td>
                  <input name="back" defaultValue={data.back} />
                </td>
              </tr>
              <tr>
                <th>Hint</th>
                <td>
                  <input name="hint" defaultValue={data.hint} />
                </td>
              </tr>
              <tr>
                <th>Extra Info</th>
                <td>
                  <input name="extraInfo" defaultValue={data.extraInfo} />
                </td>
              </tr>
            </tbody>
          </table>
          <div>
            <div className="buttons">
              <button type="submit">Save</button>
              &nbsp;&nbsp;&nbsp;
              <button type="button" onClick={handleCancel}>
                Cancel
              </button>
              &nbsp;&nbsp;&nbsp;
              <button type="button" onClick={handleDelete}>
                Delete
              </button>
            </div>
            <span className="timeInfo">
              <b>Created:</b> {timestampToDate(data.createdTs)}{" "}
              <b>Last edited:</b>
              {timestampToDate(data.lastEditedTs)}
            </span>
          </div>
        </form>
      )}
    </div>
  );
};

export default Note;
