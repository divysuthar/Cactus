import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/home.jsx";
import Upload from "./pages/Upload.jsx";
import OutputSelection from "./pages/OutputSelection.jsx";
import Result from "./pages/result.jsx";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 text-gray-900">
        <nav className="p-4 bg-blue-600 text-white text-center">
          <Link to="/" className="text-xl font-bold">Paper to X</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/output-selection" element={<OutputSelection/>} />
          <Route path="/result" element={<Result />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;