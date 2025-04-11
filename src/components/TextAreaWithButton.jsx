import './TextAreaWithButton.css'
import TextArea from './TextArea';
import Button from './Button';
export default function TextAreaWithButton () {
    return (
      <div className="textarea-with-button">
        <TextArea />
        <Button className="embedded-button" />
      </div>
    );
  };
  
