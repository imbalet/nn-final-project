import './TextAreaWithButton.css'
import TextArea from './TextArea';
import Button from './Button';
import { useNavigate } from 'react-router-dom';

export default function TextAreaWithButton () {
  const navigate = useNavigate();

  // Обработчик клика для кнопки
  const handleAnalyzeClick = () => {
    // Здесь будет ваша логика обработки данных
    // Пока просто делаем переход
    navigate('/summary');
  };


    return (
      <div className="textarea-with-button">
        <TextArea />
        <Button className="embedded-button" onClick={handleAnalyzeClick} />
      </div>
    );
  };
  
