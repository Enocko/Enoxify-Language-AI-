import React, { useState } from 'react';
import { FileText, Upload, Download, Clock, TrendingUp } from 'lucide-react';

interface DocumentResult {
  original_format: string;
  output_formats: string[];
  simplified_text?: string;
  audio_file_path?: string;
  processing_time?: number;
  file_size?: number;
}

const DocumentProcessor: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<DocumentResult | null>(null);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.type === 'application/pdf' || 
          selectedFile.name.endsWith('.docx') || 
          selectedFile.name.endsWith('.doc')) {
        setFile(selectedFile);
        setError('');
      } else {
        setError('Please select a PDF or Word document (.pdf, .docx, .doc)');
        setFile(null);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setIsProcessing(true);
    setError('');
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/process-document', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownloadSummary = () => {
    if (result) {
      const content = `Document Analysis Summary\n\nFile Format: ${result.original_format}\nOutput Formats: ${result.output_formats.join(', ')}\nFile Size: ${result.file_size ? `${(result.file_size / 1024).toFixed(1)} KB` : 'N/A'}\nProcessing Time: ${result.processing_time ? `${result.processing_time.toFixed(2)}s` : 'N/A'}\n\nSimplified Text:\n${result.simplified_text || 'Not available'}\n\nAudio Output: ${result.audio_file_path ? 'Available' : 'Not available'}`;
      
      const blob = new Blob([content], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `analysis_${result.original_format}.txt`;
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div className="p-8">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center justify-center">
          <FileText className="mr-3 h-8 w-8 text-blue-600" />
          Document Processor
        </h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="documentFile" className="block text-sm font-medium text-gray-700 mb-2">
            Document File
          </label>
          <div className="flex items-center space-x-4">
            <input
              type="file"
              id="documentFile"
              accept=".pdf,.docx,.doc"
              onChange={handleFileChange}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isProcessing}
            />
            {file && (
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Upload className="h-4 w-4" />
                <span>{file.name}</span>
              </div>
            )}
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Supported formats: PDF, Word documents (.pdf, .docx, .doc)
          </p>
        </div>

        <button
          type="submit"
          disabled={isProcessing || !file}
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 focus:ring-4 focus:ring-blue-300 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isProcessing ? 'Processing...' : 'Analyze Document'}
        </button>
      </form>

      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {result && (
        <div className="mt-8 p-6 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-xl">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-semibold text-gray-900">Analysis Results</h3>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center">
                <Clock className="mr-1 h-4 w-4" />
                {result.processing_time ? `${result.processing_time.toFixed(2)}s` : 'N/A'}
              </div>
              <div className="flex items-center">
                <TrendingUp className="mr-1 h-4 w-4" />
                {result.file_size ? `${(result.file_size / 1024).toFixed(1)} KB` : 'N/A'}
              </div>
            </div>
          </div>
          
          <div className="space-y-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Document Information:</h4>
              <div className="bg-white p-4 rounded-lg border">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-gray-600">File Format:</span>
                    <p className="text-gray-800">{result.original_format}</p>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Output Formats:</span>
                    <p className="text-gray-800">{result.output_formats.join(', ')}</p>
                  </div>
                  <div>
                    <span className="font-medium text-gray-600">File Size:</span>
                    <p className="text-gray-800">{result.file_size ? `${(result.file_size / 1024).toFixed(1)} KB` : 'N/A'}</p>
                  </div>
                  <div>
                    <span className="font-medium text-gray-600">Processing Time:</span>
                    <p className="text-gray-800">{result.processing_time ? `${result.processing_time.toFixed(2)}s` : 'N/A'}</p>
                  </div>
                </div>
              </div>
            </div>
            
            {result.simplified_text && (
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Simplified Text:</h4>
                <div className="bg-white p-4 rounded-lg border">
                  <p className="text-gray-800 leading-relaxed">{result.simplified_text}</p>
                </div>
              </div>
            )}
            
            {result.audio_file_path && (
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Audio Output:</h4>
                <div className="bg-white p-4 rounded-lg border">
                  <div className="flex items-center space-x-4">
                    <audio controls className="flex-1">
                      <source src={`http://localhost:8000/download/${result.audio_file_path}`} type="audio/mpeg" />
                      Your browser does not support the audio element.
                    </audio>
                    <a 
                      href={`http://localhost:8000/download/${result.audio_file_path}`}
                      download="document_audio.mp3"
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Download Audio
                    </a>
                  </div>
                </div>
              </div>
            )}
            
            <div className="text-center">
              <button
                onClick={handleDownloadSummary}
                className="inline-flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <Download className="h-4 w-4" />
                Download Analysis Summary
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DocumentProcessor;
