import React from "react";
import { Presentation, Radio, Video, FileText, ArrowLeft, ExternalLink } from "lucide-react";

const OutputSelection = () => {
  const outputFormats = [
    {
      title: "Presentation",
      icon: Presentation,
      description: "Convert your paper into engaging slides with key points and visuals",
      color: "bg-green-600",
      hoverColor: "hover:bg-green-700",
      features: ["Key points extraction", "Visual summaries", "Speaker notes"]
    },
    {
      title: "Podcast Script",
      icon: Radio,
      description: "Transform your research into a conversational audio script",
      color: "bg-purple-600",
      hoverColor: "hover:bg-purple-700",
      features: ["Engaging narrative", "Clear structure", "Natural transitions"]
    },
    {
      title: "Video Script",
      icon: Video,
      description: "Create a compelling video script with visuals and narration",
      color: "bg-red-600",
      hoverColor: "hover:bg-red-700",
      features: ["Visual directions", "Timed segments", "Engaging storytelling"]
    },
    {
      title: "Blog Post",
      icon: FileText,
      description: "Convert your research into an easy-to-read blog article",
      color: "bg-blue-600",
      hoverColor: "hover:bg-blue-700",
      features: ["SEO-friendly", "Rich examples", "Clear sections"]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-blue-50 py-16 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Output Format
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Select how you want to transform your research paper. Each format is optimized for different purposes and audiences.
          </p>
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center max-w-6xl mx-auto mb-8">
          <button
            onClick={() => window.location.href = '/upload'}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Upload
          </button>
        </div>

        {/* Output Format Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {outputFormats.map((format, index) => (
            <button
              key={index}
              onClick={() => window.location.href = '/result'}
              className={`p-6 rounded-xl shadow-sm hover:shadow-md transition-all ${format.color} ${format.hoverColor} text-white text-left`}
            >
              <div className="flex items-start gap-4">
                <format.icon className="w-8 h-8 mt-1" />
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold mb-2">{format.title}</h2>
                    <ExternalLink className="w-5 h-5 opacity-75" />
                  </div>
                  <p className="text-white/90 mb-4">{format.description}</p>
                  <div className="space-y-2">
                    {format.features.map((feature, featureIndex) => (
                      <div key={featureIndex} className="flex items-center gap-2 text-sm text-white/80">
                        <div className="w-1.5 h-1.5 rounded-full bg-white/80" />
                        {feature}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default OutputSelection;