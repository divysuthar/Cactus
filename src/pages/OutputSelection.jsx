import React from "react";
import { Link } from "react-router-dom";

const OutputSelection = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold">Select Output Format</h1>
      <div className="mt-4 space-y-2">
        <Link to="/result" className="block px-4 py-2 bg-green-500 text-white rounded-lg">
          Generate PPT
        </Link>
        <Link to="/result" className="block px-4 py-2 bg-purple-500 text-white rounded-lg">
          Generate Podcast
        </Link>
        <Link to="/result" className="block px-4 py-2 bg-red-500 text-white rounded-lg">
          Generate Video
        </Link>
      </div>
    </div>
  );
};

export default OutputSelection;
