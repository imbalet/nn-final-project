import './SummaryDisplay.css';


export default function SummaryDisplay({ transcription }) {
    const formatTime = (seconds) => {
        const secs = (Math.floor(seconds % 60)).toString().padStart(2, '0');
        const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
        const hours = Math.floor(minutes / 60);
        return `${hours ? hours : ""} ${minutes}:${secs}`;
    };

    return (
        <div className="summary-display">
            <h2 className="summary-title">Саммари</h2>
            <ul className="summary-list">
                {transcription?.map((item, index) => (
                    <li key={index} className="summary-item">
                        <p className="summary-time">
                            {formatTime(item.start)} - {formatTime(item.end)}
                        </p>
                        <p className="summary-text">{item.text}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}