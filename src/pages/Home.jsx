import React from "react";
import { FileText, ArrowRight, Book, Video, Presentation, Newspaper } from "lucide-react";

const Home = () => {
  const features = [
    { icon: Book, title: "Summaries", description: "Get concise summaries of research papers" },
    { icon: Video, title: "Video Scripts", description: "Convert papers into engaging video content" },
    { icon: Presentation, title: "Presentations", description: "Create slide decks from academic papers" },
    { icon: Newspaper, title: "Blog Posts", description: "Transform research into readable blog articles" }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-blue-50">
      <div className="max-w-6xl mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center space-y-6 mb-16">
          <h1 className="text-5xl font-bold text-gray-900 tracking-tight">
            Transform Research Papers into
            <span className="block text-blue-600 mt-2">Engaging Content</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Upload any research paper and convert it into various formats. Save time and make research more accessible.
          </p>
          <button 
            onClick={() => window.location.href = '/upload'}
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-lg hover:shadow-xl"
          >
            <FileText className="w-5 h-5" />
            Upload Your Paper
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <div 
              key={index} 
              className="bg-white p-6 rounded-lg border-2 border-gray-100 hover:border-blue-200 transition-colors shadow-sm hover:shadow-md"
            >
              <feature.icon className="w-12 h-12 text-blue-600 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Home;