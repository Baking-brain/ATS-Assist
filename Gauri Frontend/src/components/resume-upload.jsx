import { useState, useRef } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import "./resume-upload.css"; // Import the new CSS file

export default function ResumeUpload() {
  const [isOpen, setIsOpen] = useState(false);
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      console.log("File selected:", file.name);
    }
  };

  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className={`resume-upload ${isOpen ? "open" : "closed"}`}>
      <button onClick={() => setIsOpen(!isOpen)} className="upload-button">
        Resume Upload
        {isOpen ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
      </button>
      <div className="upload-container">
        <h2 className="upload-title">Upload your Resume</h2>
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileUpload} 
          accept=".pdf,.doc,.docx" 
          className="file-input" 
        />
        <button onClick={handleButtonClick} className="upload-file-button">
          {selectedFile ? selectedFile.name : "Click to upload resume"}
        </button>
      </div>
    </div>
  );
}
