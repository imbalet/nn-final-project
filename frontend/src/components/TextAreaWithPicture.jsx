import './TextAreaWithPicture.css';

export default function TextAreaWithPicture({ videoPreview, videoTitle, url }) {

    if (!videoPreview) return null;

    const handleClick = () => {
        window.open(url, '_blank');
    };

    return (
        <div
            className="video-container"
            title={url}
        >
            {videoPreview && (
                <img
                    src={videoPreview}
                    alt="Превью видео"
                    className="video-preview"
                    onClick={handleClick}
                    style={{ cursor: 'pointer' }}
                />
            )}
            <div className='video-title'>
                <h2>{videoTitle}</h2>
            </div>
        </div>
    );
}