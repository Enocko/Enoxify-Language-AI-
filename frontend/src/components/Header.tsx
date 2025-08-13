import React from 'react';

const Header = () => {
  return (
    <header className="bg-black/60 backdrop-blur-md border-b border-white/20 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="text-center md:text-left mb-4 md:mb-0">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
              Enoxify
            </h1>
            <p className="text-white/80 text-lg">
              AI-Powered Text Enhancement & Accessibility Platform
            </p>
          </div>
          
          <div className="flex items-center space-x-6">
            {/* Removed OpenAI GPT-4 text and status indicator */}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
