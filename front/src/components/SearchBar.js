import { useSearchParams } from 'react-router-dom';

export default function SearchBar() {
  const [search, setSearch] = useSearchParams();

  const onSearchChange = () => {
    const text = document.getElementById('search').value;

    if (text.length === 0) {
      search.delete('search');
      setSearch(search, {
        replace: true,
      });
    } else {
      search.set('search', text);
      setSearch(search, {
        replace: true,
      });
    }
  }

  return (
    <div className={'flex searchbar'}>
      <label htmlFor="search" className="flex mr2">
      </label>
      <input
        onKeyDown={(e)=> e.keyCode === 13 && onSearchChange()}
        defaultValue={search.get('search') ?? ''}
        id="search"
        name="search"
        className="searchbar__input"
        type="search"
        placeholder="Пошук компаній по назві..."
      />
      <button onClick={onSearchChange} className="searchbar__button">Пошук</button>
    </div>
  );
}