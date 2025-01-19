const Definition = ({ definitions }) => {
  if (typeof definitions === "undefined") {
    return (
      <div>
        <p>(no definition)</p>
      </div>
    );
  }
  return (
    <div>
      <ol>
        {definitions.map((definition, index) => (
          <li key={index}>{definition}</li>
        ))}
      </ol>
    </div>
  );
};

export default Definition;
