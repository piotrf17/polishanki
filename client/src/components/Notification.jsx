const Notification = ({ message, setErrorMessage }) => {
  if (message === null) {
    return null;
  }

  return (
    <div className="error">
      <button
        onClick={() => {
          setErrorMessage(null);
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
