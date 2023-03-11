export default function FilterToggle({
    visible,
    active,
    onClear,
    onApply,
  }){
    if (active) {
      return (
        <button onClick={onClear} className="btn ph3 pv1 br3 f6 ba b--moon-gray product__filter__button">
          Очистити фільтр
        </button>
      );
    }
  
    if (visible) {
      return (
        <button onClick={onApply} className="btn ph3 pv1 br3 f6 ba b--moon-gray product__filter__button">
          Фільтрувати
        </button>
      );
    }
  
    return null;
  }