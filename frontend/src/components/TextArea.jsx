import './TextArea.css'

export default function TextArea({ rows = 5, cols = 33, placeholder, onChange, value, onKeyDown, currentUrl }) {
  return (
    <textarea 
      className='textarea'
      id="url"
      name="url"
      rows={rows}
      cols={cols}
      placeholder={placeholder || "Вставьте сюда ссылку с видео на Youtube"}
      onChange={(e) => onChange(e.target.value)}
      value={value}
      onKeyDown={onKeyDown}
      currentUrl= {currentUrl}
    />
  );
}