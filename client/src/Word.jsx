import {
  useParams
} from 'react-router-dom'

const Word = () => {
  const word = useParams().word;
  return (
    <>
      <h2>{word}</h2>
    </>
  )
}

export default Word;