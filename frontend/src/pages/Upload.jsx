import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileUp, Upload as UploadIcon, AlertCircle, CheckCircle } from "lucide-react";

const Upload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === "application/pdf") {
      setFile(selectedFile);
      setError(null);
    } else {
      setError("Please select a PDF file");
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === "dragenter" || e.type === "dragover");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type === "application/pdf") {
      setFile(droppedFile);
      setError(null);
    } else {
      setError("Please drop a PDF file");
    }
  };

  const uploadPDF = async () => {
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("File uploaded successfully:", data);
      
      // Navigate to the next page with the file ID
      navigate('/output-selection', { state: { fileId: data.id } });
    } catch (error) {
      console.error("Error uploading file:", error);
      setError(error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-blue-50 py-16 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Upload Your Research Paper
          </h1>
          <p className="text-lg text-gray-600">
            Upload your PDF file to begin the conversion process
          </p>
        </div>

        <div
          className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 hover:border-blue-400"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <FileUp className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <label className="block mb-4">
            <span className="text-gray-700">
              Drag and drop your PDF here, or
              <button
                onClick={() => document.querySelector('input[type="file"]').click()}
                className="text-blue-600 hover:text-blue-700 font-medium mx-1"
              >
                browse
              </button>
              to choose a file
            </span>
            <input
              type="file"
              className="hidden"
              onChange={handleFileChange}
              accept="application/pdf"
            />
          </label>
          {file && (
            <div className="text-sm text-gray-600 bg-gray-100 p-2 rounded">
              Selected: {file.name}
            </div>
          )}
        </div>

        <div className="mt-6 space-y-4">
          {error && (
            <div className="flex items-center gap-2 text-red-600 bg-red-50 p-3 rounded">
              <AlertCircle className="w-5 h-5" />
              {error}
            </div>
          )}

          <div className="flex justify-center gap-4">
            <button
              onClick={uploadPDF}
              disabled={uploading || !file}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg text-white transition-colors ${
                uploading || !file
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700"
              }`}
            >
              <UploadIcon className="w-5 h-5" />
              {uploading ? "Uploading..." : "Upload PDF"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;