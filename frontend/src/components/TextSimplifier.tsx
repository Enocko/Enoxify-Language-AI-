import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface SimplificationResult {
  originalText: string;
  simplifiedText: string;
  readingLevel: string;
}

const TextSimplifier = () => {
  const { token } = useAuth();
  const [text, setText] = useState('');
  const [readingLevel, setReadingLevel] = useState('elementary');
  const [result, setResult] = useState<SimplificationResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleExampleClick = (example: string) => {
    setText(example);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/simplify-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          text: text.trim(),
          target_level: readingLevel,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult({
          originalText: text,
          simplifiedText: data.simplified_text,
          readingLevel: readingLevel,
        });
      } else {
        console.error('Failed to simplify text');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const examples = [
    "The quantum mechanical properties of subatomic particles exhibit wave-particle duality, whereby they can manifest characteristics of both waves and particles depending on the method of observation employed.",
    "The intricate interplay between socioeconomic factors and educational attainment manifests in complex patterns of academic achievement across diverse demographic populations.",
    "The implementation of sustainable development practices necessitates a comprehensive understanding of environmental, economic, and social interdependencies."
  ];

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">Text Simplifier</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Transform complex text into clear, accessible language for different reading levels.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
            Enter your text
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={6}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            placeholder="Paste your complex text here..."
            required
          />
        </div>

        <div>
          <label htmlFor="reading-level" className="block text-sm font-medium text-gray-700 mb-2">
            Target reading level
          </label>
          <select
            id="reading-level"
            value={readingLevel}
            onChange={(e) => setReadingLevel(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="elementary">Elementary (Ages 6-10)</option>
            <option value="middle_school">Middle School (Ages 11-13)</option>
            <option value="high_school">High School (Ages 14-18)</option>
            <option value="college">College (Ages 18+)</option>
          </select>
        </div>

        <div className="text-center">
          <button
            type="submit"
            disabled={isLoading || !text.trim()}
            className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 focus:ring-4 focus:ring-blue-300 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Simplifying...' : 'Simplify Text'}
          </button>
        </div>
      </form>

      {/* Example Texts */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Try these examples:</h3>
        <div className="space-y-3">
          {examples.map((example, index) => (
            <button
              key={index}
              onClick={() => handleExampleClick(example)}
              className="block w-full text-left p-3 text-sm text-gray-600 bg-white rounded border hover:bg-gray-50 transition-colors"
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white border border-gray-200 rounded-lg p-6 space-y-4">
          <div className="text-center">
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              Simplified for {result.readingLevel.replace('_', ' ')} level
            </h3>
            <div className="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
              {result.readingLevel.replace('_', ' ')}
            </div>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Original Text</h4>
              <div className="p-3 bg-gray-50 rounded border text-gray-700 text-sm">
                {result.originalText}
              </div>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Simplified Text</h4>
              <div className="p-3 bg-blue-50 rounded border text-gray-700 text-sm">
                {result.simplifiedText}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TextSimplifier;
