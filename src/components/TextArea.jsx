import './TextArea.css'

export default function TextArea() {
    return (
      <textarea className='textarea'
        id="story"
        name="story"
        rows="5"
        cols="33"
        placeholder="Вставьте сюда ссылку с видео на Youtube"
      />
    );
  }