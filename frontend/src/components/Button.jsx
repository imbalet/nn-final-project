import './Button.css';

// Добавляем пропсы className и onClick
export default function Button({ className, onClick }) {
  return(
    <button 
      className={`textarea-button ${className || ''}`} 
      onClick={onClick} 
    >
      <svg
        width="35"
        height="35"
        viewBox="0 0 24 24"
        style={{ display: 'block', margin: 'auto' }}
      >
        <path
          d="M5 12H19M19 12L12 5M19 12L12 19"
          stroke="currentColor"
          strokeWidth="2"
        />
      </svg>
    </button>
  );
}