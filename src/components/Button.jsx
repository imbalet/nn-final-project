import './Button.css'
export default function Button(){
    return(
        <button className="textarea-button">
        <svg
          width="30"
          height="30"
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
    )
}