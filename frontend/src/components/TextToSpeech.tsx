import React, { useState, useRef, useEffect } from 'react';
import { Download, Play, Pause } from 'lucide-react';

interface TTSResult {
  audio_file_path: string;
  duration: number;
  text: string;
  translated_text?: string;
  language: string;
}

const TextToSpeech: React.FC = () => {
  const [text, setText] = useState('');
  const [voice, setVoice] = useState('neutral'); // Voice type for backend (male, female, neutral)
  const [selectedVoiceId, setSelectedVoiceId] = useState('us_english'); // New state for dropdown value
  const [selectedLanguage, setSelectedLanguage] = useState('en-US'); // Language code for backend
  const [speed, setSpeed] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<TTSResult | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioElement = useRef<HTMLAudioElement>(null);

  const voiceOptions = [
    { id: 'us_english', value: 'neutral', label: '🇺🇸 US English', description: 'American English accent', language: 'en-US' },
    { id: 'uk_english', value: 'neutral', label: '🇬🇧 UK English', description: 'British English accent', language: 'en-GB' },
    { id: 'spanish', value: 'neutral', label: '🇪🇸 Spanish', description: 'Speaks in Spanish language', language: 'es' },
    { id: 'french', value: 'neutral', label: '🇫🇷 French', description: 'Speaks in French language', language: 'fr' },
    { id: 'german', value: 'neutral', label: '🇩🇪 German', description: 'Speaks in German language', language: 'de' }
  ];

  // Set initial language on mount
  useEffect(() => {
    const selectedOption = voiceOptions.find(option => option.id === selectedVoiceId);
    if (selectedOption) {
      console.log('DEBUG: Initial language setup:', selectedOption.language);
      setSelectedLanguage(selectedOption.language);
    }
  }, [selectedVoiceId, voiceOptions]); // Add dependencies

  // Update selectedLanguage when selectedVoiceId changes
  useEffect(() => {
    const selectedOption = voiceOptions.find(option => option.id === selectedVoiceId);
    if (selectedOption) {
      console.log('DEBUG: Updating selectedLanguage to:', selectedOption.language);
      setSelectedLanguage(selectedOption.language);
    }
  }, [selectedVoiceId, voiceOptions]); // Remove selectedLanguage to avoid infinite loop

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;

    console.log('DEBUG: Submitting TTS request with language:', selectedLanguage);
    console.log('DEBUG: Selected voice ID:', selectedVoiceId);

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/text-to-speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text, 
          voice, 
          speed: 1.0, // Always generate at 1x speed
          language: selectedLanguage // Use the selected language
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('DEBUG: TTS response:', data);
        setResult(data);
      } else {
        console.error('TTS request failed');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlayAudio = () => {
    if (audioElement.current) {
      if (isPlaying) {
        audioElement.current.pause();
        setIsPlaying(false);
      } else {
        // Set the playback rate before playing
        audioElement.current.playbackRate = speed;
        audioElement.current.play();
        setIsPlaying(true);
      }
    }
  };

  const handleSpeedSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newSpeed = parseFloat(e.target.value);
    setSpeed(newSpeed);
    
    // If audio is currently playing, update the playback rate immediately
    if (audioElement.current && isPlaying) {
      audioElement.current.playbackRate = newSpeed;
    }
  };

  const handleVoiceChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    console.log('DEBUG: Voice dropdown changed to:', e.target.value);
    setSelectedVoiceId(e.target.value);
  };

  return (
    <div className="p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Text to Speech</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="text" className="block text-sm font-medium text-gray-700 mb-2">
            Enter Text
          </label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type or paste your text here..."
            className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            required
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="voice" className="block text-sm font-medium text-gray-700 mb-2">
              Voice & Language
            </label>
            <select
              id="voice"
              value={selectedVoiceId}
              onChange={handleVoiceChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {voiceOptions.map((option) => (
                <option key={option.id} value={option.id}>
                  {option.label} - {option.description}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="speed" className="block text-sm font-medium text-gray-700 mb-2">
              Playback Speed: {speed}x
            </label>
            <input
              type="range"
              id="speed"
              min="0.5"
              max="2"
              step="0.25"
              value={speed}
              onChange={handleSpeedSliderChange}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0.5x</span>
              <span>1x</span>
              <span>1.5x</span>
              <span>2x</span>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading || !text.trim()}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
        >
          {isLoading ? 'Generating Speech...' : 'Convert to Speech'}
        </button>
      </form>

      {result && (
        <div className="mt-8 p-6 bg-gradient-to-r from-green-50 to-blue-50 rounded-xl border border-green-200">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Generated Speech</h3>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Original Text:</h4>
              <p className="text-gray-600 bg-white p-3 rounded-lg border">{result.text}</p>
            </div>
            
            {result.translated_text && (
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Translated Text (for speech):</h4>
                <p className="text-gray-600 bg-white p-3 rounded-lg border">{result.translated_text}</p>
              </div>
            )}
            
            {result.translated_text && (
              <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                <p className="text-sm text-blue-800">
                  <strong>Note:</strong> Your text has been automatically translated to {voiceOptions.find(v => v.language === result.language)?.label.split(' ')[1]} for natural speech in that language.
                </p>
                <p className="text-sm text-blue-700 mt-2">
                  <strong>Language:</strong> The audio will speak in {voiceOptions.find(v => v.language === result.language)?.label.split(' ')[1]} language, not English with an accent.
                </p>
              </div>
            )}
            
            <div className="flex items-center justify-between bg-white p-4 rounded-lg border">
              <div className="flex items-center space-x-4">
                <button
                  onClick={handlePlayAudio}
                  className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-300 transition-colors"
                >
                  {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                  <span>{isPlaying ? 'Pause' : 'Play'}</span>
                </button>
                <span className="text-sm text-gray-600">
                  Duration: ~{Math.round(result.duration)}s | Speed: {speed}x | Language: {voiceOptions.find(v => v.language === result.language)?.label.split(' ')[1] || result.language}
                </span>
              </div>
              
              <a
                href={`http://localhost:8000/download/${result.audio_file_path}`}
                download
                className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 focus:ring-2 focus:ring-green-300 transition-colors"
              >
                <Download size={16} />
                <span>Download</span>
              </a>
            </div>
          </div>
          
          <audio
            ref={audioElement}
            src={`http://localhost:8000/download/${result.audio_file_path}`}
            onEnded={() => setIsPlaying(false)}
            onPause={() => setIsPlaying(false)}
            onPlay={() => setIsPlaying(true)}
            className="hidden"
          />
        </div>
      )}
    </div>
  );
};

export default TextToSpeech;
