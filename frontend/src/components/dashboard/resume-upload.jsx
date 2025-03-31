// import { useState, useRef } from "react";
// import { ChevronDown, ChevronUp } from "lucide-react";
// import "./resume-upload.css";

// export default function ResumeUpload() {
//   const [isOpen, setIsOpen] = useState(false);
//   const fileInputRef = useRef(null);
//   const [selectedFile, setSelectedFile] = useState(null);

//   const handleFileUpload = (event) => {
//     const file = event.target.files?.[0];
//     if (file) {
//       setSelectedFile(file);
//       console.log("File selected:", file.name);
//     }
//   };

//   const handleButtonClick = () => {
//     if (fileInputRef.current) {
//       fileInputRef.current.click();
//     }
//   };

//   return (
//     <div className={`resume-upload ${isOpen ? "open" : "closed"}`}>
//       <button onClick={() => setIsOpen(!isOpen)} className="upload-drop">
//         Resume Upload
//         {isOpen ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
//       </button>
//       <div className="upload-container">
//         <h2 className="upload-title">Upload your Resume</h2>
//         <input
//           type="file"
//           ref={fileInputRef}
//           onChange={handleFileUpload}
//           accept=".pdf,.doc,.docx"
//           className="file-input"
//         />
//         <button onClick={handleButtonClick} className="upload-file-button">
//           {selectedFile ? selectedFile.name : "Click to upload resume"}
//         </button>
//       </div>
//     </div>
//   );
// }

import { useState, useRef } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import axios from "axios";
import "./resume-upload.css";

export default function ResumeUpload() {
  const [isOpen, setIsOpen] = useState(false);
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragging, setDragging] = useState(false);

  // Handle file selection via input
  const handleFileUpload = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      console.log("File selected:", file.name);
    }
  };

  // Handle clicking the button to open file input
  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  // Handle drag over event to allow file drop
  const handleDragOver = (event) => {
    event.preventDefault(); // Prevent default behavior (prevent opening file)
    setDragging(true);
  };

  // Handle drag leave event to reset the area after drag leaves
  const handleDragLeave = () => {
    setDragging(false);
  };

  // Handle file drop event
  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    if (file) {
      setSelectedFile(file);
      console.log("File dropped:", file.name);
    }
    setDragging(false);
  };

  async function submitFile() {
    if (!selectedFile) return;

    console.log(selectedFile.name);
    setIsOpen(false);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const uploadFileResponse = await axios.post("api/file_upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("File uploaded successfully", uploadFileResponse.data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  }

  return (
    <div className={`resume-upload ${isOpen ? "open" : "closed"}`}>
      <button onClick={() => setIsOpen(!isOpen)} className="upload-drop">
        Resume Upload
        {isOpen ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
      </button>

      <div className="upload-content">
        {isOpen && (
          <>
            <div className="upload-container">
              <h2 className="upload-title">Upload your Resume</h2>

              {/* Drag and Drop Area */}
              <div
                className={`drag-area ${dragging ? "dragging" : ""}`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={handleButtonClick}
                onDragLeave={handleDragLeave}
              >
                {selectedFile ? (
                  <p className="file-name">{selectedFile.name}</p>
                ) : (
                  <p>Drag & Drop your Resume here or click to select</p>
                )}

                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept=".pdf,.doc,.docx"
                  className="file-input"
                />
                {/* <button
                  onClick={handleButtonClick}
                  className="upload-file-button"
                >
                  {selectedFile ? selectedFile.name : "Click to upload resume"}
                </button> */}
              </div>
            </div>

            {/* Custom Action Button */}
            {selectedFile && (
              <div className="action-container">
                <button
                  className="custom-action-button"
                  onClick={() => submitFile()}
                >
                  Custom Action
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
