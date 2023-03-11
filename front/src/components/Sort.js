export default function Sort({
    options,
    name,
    defaultValue = '',
    onChange,
  }){
    return (
        <select
          onChange={onChange}
          name={name}
          defaultValue={defaultValue}
          className="pv1 products__sort"
        >
          {options.map((option, key) => (
            <option key={key} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
    );
  }