import { useState } from "react";

const Notification = ({ message }) => {
  const [hidden, setHidden] = useState(false);

  if (message === null || hidden) {
    return null;
  }

  return (
    <div className="error">
      <button
        onClick={() => {
          setHidden(true);
        }}
      >
        x
      </button>
      &nbsp; &nbsp; &nbsp; &nbsp;
      {message}
    </div>
  );
};

export default Notification;
