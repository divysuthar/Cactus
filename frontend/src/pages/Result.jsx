import React, { useState } from 'react';
import { Download, Check, FileDown } from 'lucide-react';

const Result = () => {
  const [isDownloading, setIsDownloading] = useState(false);
  const [isDownloaded, setIsDownloaded] = useState(false);

  const handleDownload = () => {
    setIsDownloading(true);
 
    setTimeout(() => {
      setIsDownloading(false);
      setIsDownloaded(true);
      setTimeout(() => setIsDownloaded(false), 2000);
    }, 1500);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-6">
      <div className="bg-white rounded-xl shadow-lg p-8 max-w-md w-full space-y-6 text-center">
        <div className="mb-6">
          <div className="bg-blue-100 p-4 rounded-full inline-block">
            <FileDown className="w-8 h-8 text-blue-600" />
          </div>
        </div>

        <h1 className="text-3xl font-bold text-gray-900">Ready for Download</h1>
        
        <p className="text-gray-600 text-lg">
          Your file has been processed and is ready to be downloaded
        </p>

        <button
          onClick={handleDownload}
          disabled={isDownloading}
          className={`
            w-full flex items-center justify-center gap-2 
            px-6 py-3 rounded-lg font-medium
            transform transition-all duration-200
            ${isDownloading ? 
              'bg-blue-400 cursor-wait' : 
              'bg-blue-600 hover:bg-blue-700 hover:-translate-y-0.5 active:translate-y-0'
            }
            text-white shadow-lg hover:shadow-xl
          `}
        >
          {isDownloading ? (
            <>
              <div className="w-5 h-5 border-t-2 border-white rounded-full animate-spin" />
              <span>Downloading...</span>
            </>
          ) : isDownloaded ? (
            <>
              <Check className="w-5 h-5" />
              <span>Downloaded!</span>
            </>
          ) : (
            <>
              <Download className="w-5 h-5" />
              <span>Download File</span>
            </>
          )}
        </button>

        <p className="text-sm text-gray-500">
          Having trouble? <a href="#" className="text-blue-600 hover:underline">Contact support</a>
        </p>
      </div>
    </div>
  );
};

export default Result;