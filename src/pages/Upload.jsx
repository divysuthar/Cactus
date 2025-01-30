import React, { useState } from "react";
import { Link } from "react-router-dom";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [fileId, setFileId] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const convertToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = (error) => reject(error);
    });
  };

  const uploadPDF = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const base64File = await convertToBase64(file);

      const response = await fetch("https://679b818133d3168463241a20.mockapi.io/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ file: base64File, fileName: file.name }),
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("File uploaded successfully:", data);

      setFileId(data.id); // Using MockAPI's generated ID
    } catch (error) {
      console.error("Error uploading file:", error);
      setError(error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold">Upload Research Paper</h1>
      <input type="file" className="mt-4 p-2 border" onChange={handleFileChange} />
      <button
        onClick={uploadPDF}
        className="mt-4 px-4 py-2 bg-green-600 text-white rounded-lg"
        disabled={uploading}
      >
        {uploading ? "Uploading..." : "Upload"}
      </button>
      {error && <p className="mt-2 text-red-500">{error}</p>}
      {fileId && <p className="mt-2 text-green-500">Upload successful! File ID: {fileId}</p>}
      <Link to="/output-selection" className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg">
        Next
      </Link>
    </div>
  );
};

export default Upload;
