const Definition = ({ definitions }) => {
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
