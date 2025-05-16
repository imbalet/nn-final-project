import img from '/src/assets/button.svg';

// Добавляем пропсы className и onClick
export default function Button({ className, onClick }) {
  return(
    <button 
      className={`textarea-button ${className || ''}`} 
      onClick={onClick} 
    >

    <img src={img} className='but'></img>
    </button>
  );
}