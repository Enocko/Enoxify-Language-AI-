import React, { useState } from 'react';
import Header from './components/Header';
import TextSimplifier from './components/TextSimplifier';
import TextToSpeech from './components/TextToSpeech';
import SpeechToText from './components/SpeechToText';
import DocumentProcessor from './components/DocumentProcessor';
import { DemoOne } from './components/ui/demo';

function App() {
  const [activeSection, setActiveSection] = useState('text-simplifier');

  const sections = [
    { id: 'text-simplifier', label: 'Text Simplifier', component: TextSimplifier },
    { id: 'text-to-speech', label: 'Text to Speech', component: TextToSpeech },
    { id: 'speech-to-text', label: 'Speech to Text', component: SpeechToText },
    { id: 'document-processor', label: 'Document Processor', component: DocumentProcessor },
  ];

  const renderActiveSection = () => {
    const section = sections.find(s => s.id === activeSection);
    if (section) {
      const Component = section.component;
      return <Component />;
    }
    return null;
  };

  return (
    <div className="min-h-screen relative flex flex-col bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900">
      {/* 3D Background */}
      <div className="fixed inset-0 z-0 opacity-80">
        <DemoOne />
      </div>
      
      {/* Content Overlay */}
      <div className="relative z-10 flex flex-col flex-1">
        <Header />
        
        <main className="container mx-auto px-4 py-8 flex-1">
          {/* Navigation Tabs */}
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                  activeSection === section.id
                    ? 'bg-white/30 text-white backdrop-blur-md border border-white/50 shadow-xl'
                    : 'bg-white/20 text-white/90 hover:bg-white/30 hover:text-white backdrop-blur-md border border-white/30 hover:border-white/50'
                }`}
              >
                {section.label}
              </button>
            ))}
          </div>

          {/* Active Section */}
          <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/40 p-8 hover:bg-white/85 transition-all duration-300">
            {renderActiveSection()}
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-black/80 backdrop-blur-md text-white py-6 mt-auto border-t border-white/20">
          <div className="container mx-auto px-4 flex justify-end items-center">
            <div className="text-sm text-gray-300">
              © 2025 Enoxify, Inc. All rights reserved.
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
