import { useState, useEffect, useRef } from 'react';
import './Summary.css';
import Header from '../components/Header';
import Footer from '../components/Footer';
import TextAreaWithButton from '../components/TextAreaWithButton';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import TextAreaWithPicture from '../components/TextAreaWithPicture';
import SummaryDisplay from '../components/SummaryDisplay';

function Summary() {
  const location = useLocation();
  const intervalRef = useRef();
  const isMounted = useRef(true);
  const { id } = useParams();
  const [transcription, setTranscription] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentUrl, setCurrentUrl] = useState(location.state?.videoUrl || '');
  const [videoPreview, setVideoPreview] = useState(null);
  const [videoTitle, setVideoTitle] = useState('');

  useEffect(() => {
    setTranscription('');
    setVideoPreview(null);
    setVideoTitle('');
    setIsLoading(true);
    setError(null);
    setCurrentUrl(location.state?.videoUrl || '');
  }, [id, location.state?.videoUrl]);

  useEffect(() => {
    isMounted.current = true;

    const fetchData = async () => {
      try {
        const response = await fetch(`/api/video/${id}/summary`);
        if (!isMounted.current) return;

        if (response.ok) {
          const data = await response.json();
          if (data.status != "pending") {
            clearInterval(intervalRef.current);
            setVideoPreview(data.preview_link);
            setVideoTitle(data.title);
            setTranscription(data.summary);
            setIsLoading(false);
            try {
              const parsedSummary = JSON.parse(data.summary);
              setTranscription(parsedSummary);
            } catch (parseError) {
              console.error('Ошибка парсинга summary:', parseError);
              setError('Ошибка формата данных');
            }
          }
        }
      } catch (error) {
        if (!isMounted.current) return;
        console.error('Ошибка запроса:', error);
      }
    };
    intervalRef.current = setInterval(fetchData, 5000);


    fetchData();
    return () => {
      isMounted.current = false;
      clearInterval(intervalRef.current);
    };
  }, [location.state?.videoUrl]);




  return (
    <div>
      <Header />
      <div className='paragraph'>
        <TextAreaWithButton
          rows={1}
          initialValue={currentUrl}
        />

        {videoPreview && (
          <TextAreaWithPicture
            videoPreview={videoPreview}
            videoTitle={videoTitle}
            url={currentUrl}
          />
        )}

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
          <SummaryDisplay
            transcription={transcription} />
        )}
      </div>
      <Footer />
    </div>
  );
}

export default Summary;