import './TextArea.css'

export default function TextArea({ rows = 5, cols = 33, placeholder }) {
  return (
    <textarea 
      className='textarea'
      id="url"
      name="url"
      rows={rows}
      cols={cols}
        placeholder={placeholder || "Вставьте сюда ссылку с видео на Youtube"}
    />
  );
}