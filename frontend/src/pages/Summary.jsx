import { useState, useEffect } from 'react';
import './Summary.css';
import Header from '../components/Header';
import Footer from '../components/Footer';
import TextArea from '../components/TextArea';
import TextAreaWithButton from '../components/TextAreaWithButton';
import { useLocation, useNavigate } from 'react-router-dom';

function Summary() {
  const location = useLocation();
  const navigate = useNavigate();
  const [transcription, setTranscription] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentUrl, setCurrentUrl] = useState(location.state?.videoUrl || '');

  useEffect(() => {
    const processVideo = async (url) => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await fetch('http://localhost:8000/process_video', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url }),
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

    if (location.state?.videoUrl) {
      processVideo(location.state.videoUrl);
    }
  }, [location.state?.videoUrl]);

  const handleNewAnalysis = (newUrl) => {
    navigate('/summary', { 
      state: { 
        videoUrl: newUrl,
        isLoading: true 
      } 
    });
    setCurrentUrl(newUrl);
  };

  return (
    <div>
      <Header />
      <div className='paragraph'>
        <TextAreaWithButton 
          rows={1}
          initialValue={currentUrl}
          onAnalyze={handleNewAnalysis}
        />
        
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