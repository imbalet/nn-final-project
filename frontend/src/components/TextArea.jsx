import './TextArea.css'

export default function TextArea({ rows = 2, cols = 2, placeholder, onChange, value, onKeyDown }) {
  return (
    <div className='textarea'>
      <textarea
        className='textarea-text'
        id="url"
        name="url"
        rows={rows}
        cols={cols}
        placeholder={placeholder || "Вставьте сюда ссылку с видео на Youtube"}
        onChange={(e) => onChange(e.target.value)}
        value={value}
        onKeyDown={onKeyDown}
      />
    </div>
  );
}