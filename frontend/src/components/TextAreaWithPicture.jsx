import './TextAreaWithPicture.css';
import { useNavigate } from 'react-router-dom'; // Для React Router

export default function TextAreaWithPicture({ videoPreview, videoTitle, url }) {
    const navigate = useNavigate();

    if (!videoPreview) return null;

    const handleClick = () => {
        window.open(url, '_blank'); // Открывает URL в новой вкладке
        // Или для React Router: navigate(url);
    };

    return (
        <div 
            className="video-container" 
            onClick={handleClick}
            style={{ cursor: 'pointer' }}
            title={url}
        >
            {videoPreview && (
                <img 
                    src={videoPreview} 
                    alt="Превью видео"
                    className="video-preview"
                />
            )}
            <div className='video-title'>
                <h3>{videoTitle}</h3>
            </div>
        </div>
    );
}