import React from "react";

const Result = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold">Generated Output</h1>
      <p className="text-lg mt-4">Your file is ready to download.</p>
      <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg">
        Download
      </button>
    </div>
  );
};

export default Result;
