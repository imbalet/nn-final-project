import img from '/src/assets/button.svg';
import './Button.css';

export default function Button({ className, onClick }) {
  return (
    <button
      className={`textarea-button ${className || ''}`}
      onClick={onClick}
    >
      <img src={img} className='confirm-button'></img>
    </button>
  );
}