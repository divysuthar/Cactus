import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-4xl font-bold">Welcome to Paper to X</h1>
      <p className="text-lg mt-4">Convert research papers into various content formats.</p>
      <Link to="/upload" className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg">
        Get Started
      </Link>
    </div>
  );
};

export default Home;
