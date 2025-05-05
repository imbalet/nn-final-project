import { useState, useEffect } from 'react';
import './TextAreaWithButton.css';
import TextArea from './TextArea';
import Button from './Button';
import { useNavigate } from 'react-router-dom';

export default function TextAreaWithButton({ rows, initialValue = '' }) {
  const [inputValue, setInputValue] = useState(initialValue);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    setInputValue(initialValue);
  }, [initialValue]);

  const handleAnalyze = async () => {
    try {
      setError(null);
      if (!inputValue.trim()) {
        setError('Пожалуйста, введите URL YouTube видео');
        return;
      }

      if (!validateUrl(inputValue.trim())) {
        setError('Пожалуйста, введите корректный URL YouTube видео');
        return;
      }

      const response = await fetch(`/api/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "url": inputValue.trim() }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Ошибка сервера');
      }

      const data = await response.json();
      const id = data.id;
      navigate(`/video/${id}/summary`, {
        state: {
          videoUrl: inputValue.trim(),
          isLoading: true
        }
      });
    }
    catch (err) {
      setError(err.message);
    }
  };

  const validateUrl = (url) => {
    const youtubeRegex = /(?:v=|\/)([0-9A-Za-z_-]{11}).*/;
    if (url.length && !youtubeRegex.test(url)) {
      return false;
    }
    setError(null);
    return true;
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAnalyze();
    }
  };

  return (
    <div className="textarea-with-button">
      <TextArea
        rows={rows}
        value={inputValue}
        onChange={(value) => {
          setInputValue(value);
          const isValid = validateUrl(value);
          setError(isValid ? null : 'Пожалуйста, введите корректный URL YouTube видео');
        }}
        onKeyDown={handleKeyPress}
      />
      {error && <div className="error-message">{error}</div>}
      <Button onClick={handleAnalyze} />
    </div>
  );
}