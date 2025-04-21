import { useState } from 'react';
import './TextAreaWithButton.css';
import TextArea from './TextArea';
import Button from './Button';
import { useNavigate } from 'react-router-dom';

export default function TextAreaWithButton({ rows }) {
  const [inputValue, setInputValue] = useState('');
  const navigate = useNavigate();

  const handleAnalyzeClick = async () => {
    if (!inputValue.trim()) {
      alert('Пожалуйста, введите URL YouTube видео');
      return;
    }
    
    // Переходим сразу на страницу результатов с передачей URL
    navigate('/summary', { 
      state: { 
        videoUrl: inputValue.trim(),
        isLoading: true 
      } 
    });
  };

  return (
    <div className="textarea-with-button">
      <TextArea 
        rows={rows}
        value={inputValue}
        onChange={(value) => setInputValue(value)}
      />
      <Button onClick={handleAnalyzeClick} />
    </div>
  );
}