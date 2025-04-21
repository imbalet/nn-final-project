import { useState, useEffect } from 'react';
import './Summary.css';
import Header from '../components/Header';
import Footer from '../components/Footer';
import TextArea from '../components/TextArea';
import { useLocation } from 'react-router-dom';

function Summary() {
  const location = useLocation();
  const [transcription, setTranscription] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const processVideo = async () => {
      try {
        const videoUrl = location.state?.videoUrl;
        if (!videoUrl) {
          throw new Error('URL видео не получен');
        }

        const response = await fetch('http://localhost:8000/process_video', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: videoUrl }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Ошибка сервера');
        }

        const data = await response.json();
        setTranscription(data.transcription);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    if (location.state?.isLoading) {
      processVideo();
    }
  }, [location]);

  return (
    <div>
      <Header />
      <div className='paragraph'>
        {isLoading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Идет обработка видео...</p>
          </div>
        ) : error ? (
          <div className="error-message">
            <p>⚠️ Ошибка: {error}</p>
          </div>
        ) : (
          <TextArea 
            value={transcription}
            readOnly
            rows={15}
          />
        )}
      </div>
      <Footer/>
    </div>
  );
}

export default Summary;