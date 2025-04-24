import { useState, useEffect } from 'react';
import './TextAreaWithButton.css';
import TextArea from './TextArea';
import Button from './Button';
import { useNavigate } from 'react-router-dom';

export default function TextAreaWithButton({ rows, initialValue = ''}) {
  const [inputValue, setInputValue] = useState(initialValue);
  const navigate = useNavigate();

  useEffect(() => {
    setInputValue(initialValue);
  }, [initialValue]);

  const handleAnalyze = () => {
    if (!inputValue.trim()) {
      alert('Пожалуйста, введите URL YouTube видео');
      return;
    }
    
    navigate('/summary', { 
      state: { 
        videoUrl: inputValue.trim(),
        isLoading: true 
      } 
    });
  };

  // Обработчик нажатия клавиш
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault(); // Предотвращаем перенос строки
      handleAnalyze();
    }
  };

  return (
    <div className="textarea-with-button">
      <TextArea 
        rows={rows}
        value={inputValue}
        onChange={(value) => setInputValue(value)}
        onKeyDown={handleKeyPress} // Добавляем обработчик клавиш
      />
      <Button onClick={handleAnalyze} />
    </div>
  );
}