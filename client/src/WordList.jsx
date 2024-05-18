import { Link } from 'react-router-dom';

const WordList = () => {
  return (
    <ul>
      <li>
        <Link to={'/words/biegać'}>biegać</Link>
      </li>
      <li>
        <Link to={'/words/gość'}>gość</Link>
      </li>
    </ul>
  )
}

export default WordList;