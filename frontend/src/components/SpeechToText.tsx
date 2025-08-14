import React, { useState, useRef } from 'react';
import { Mic, Play, Pause, Download, Square, Upload } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface STTResult {
  transcript: string;
  confidence: number;
  processing_time: number;
}

const SpeechToText: React.FC = () => {
  const { token } = useAuth();
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<STTResult | null>(null);
  const [error, setError] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  
  // New states for live recording
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [recordedChunks, setRecordedChunks] = useState<Blob[]>([]);
  const recordedChunksRef = useRef<Blob[]>([]);
  const recordingTimerRef = useRef<NodeJS.Timeout | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.type.startsWith('audio/')) {
        setAudioFile(file);
        setError('');
        setResult(null);
      } else {
        setError('Please select an audio file (MP3, WAV, M4A, FLAC)');
        setAudioFile(null);
      }
    }
  };

  const startRecording = async () => {
    try {
      console.log('Starting recording process...');
      
      // Check if MediaRecorder is supported
      if (!window.MediaRecorder) {
        setError('MediaRecorder is not supported in this browser. Please use a modern browser.');
        return;
      }
      
      // Check microphone permissions
      const permissions = await navigator.permissions.query({ name: 'microphone' as PermissionName });
      console.log('Microphone permission status:', permissions.state);
      
      if (permissions.state === 'denied') {
        setError('Microphone access is denied. Please enable microphone permissions in your browser.');
        return;
      }
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100,
          channelCount: 1
        } 
      });
      
      console.log('Microphone stream obtained:', stream.getAudioTracks().length, 'tracks');
      
      // Try to use the most compatible format first - prioritize formats the backend supports
      let mimeType = 'audio/wav';
      const supportedTypes = [
        'audio/wav',
        'audio/mp4',
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/ogg;codecs=opus',
        'audio/ogg'
      ];
      
      for (const type of supportedTypes) {
        if (MediaRecorder.isTypeSupported(type)) {
          mimeType = type;
          break;
        }
      }
      
      console.log('Using recording format:', mimeType);
      console.log('MediaRecorder.isTypeSupported for this format:', MediaRecorder.isTypeSupported(mimeType));
      
      // Clear any previous chunks
      setRecordedChunks([]);
      recordedChunksRef.current = []; // Clear the ref
      
      let recorder: MediaRecorder | null = null;
      try {
        recorder = new MediaRecorder(stream, { mimeType });
        console.log('MediaRecorder created successfully with format:', mimeType);
      } catch (error) {
        console.warn('Failed to create MediaRecorder with preferred format, trying fallback:', error);
        // Fallback to basic audio recording
        recorder = new MediaRecorder(stream);
        mimeType = recorder.mimeType || 'audio/webm';
        console.log('Using fallback format:', mimeType);
      }
      
      recorder.ondataavailable = (event) => {
        console.log('Data available:', event.data.size, 'bytes, type:', event.data.type);
        if (event.data.size > 0) {
          // Update both state and ref
          setRecordedChunks(prev => [...prev, event.data]);
          recordedChunksRef.current = [...recordedChunksRef.current, event.data];
          console.log('Chunk added, total chunks:', recordedChunksRef.current.length);
        } else {
          console.warn('Data available but size is 0');
        }
      };

      recorder.onstart = () => {
        console.log('Recording started successfully');
        setIsRecording(true);
        setRecordingTime(0);
        
        // Start timer
        recordingTimerRef.current = setInterval(() => {
          setRecordingTime(prev => prev + 1);
        }, 1000);
      };

      recorder.onstop = () => {
        console.log('Recording stopped, chunks:', recordedChunksRef.current.length);
        
        // Stop the timer
        if (recordingTimerRef.current) {
          clearInterval(recordingTimerRef.current);
          recordingTimerRef.current = null;
        }
        
        // Check if we have any data using the ref
        if (recordedChunksRef.current.length === 0) {
          console.error('No chunks recorded');
          setError('No audio data captured. Please try recording again.');
          setIsRecording(false);
          setRecordingTime(0);
          stream.getTracks().forEach(track => track.stop());
          return;
        }
        
        const audioBlob = new Blob(recordedChunksRef.current, { type: mimeType });
        console.log('Blob created:', audioBlob.size, 'bytes, type:', audioBlob.type);
        
        // Validate blob size
        if (audioBlob.size === 0) {
          console.error('Blob size is 0');
          setError('Recording failed - no audio data captured. Please try again.');
          setIsRecording(false);
          setRecordingTime(0);
          stream.getTracks().forEach(track => track.stop());
          return;
        }
        
        // Extract file extension from MIME type and ensure it's valid
        let extension = 'wav';
        if (mimeType.includes('webm')) extension = 'webm';
        else if (mimeType.includes('mp4')) extension = 'mp4';
        else if (mimeType.includes('ogg')) extension = 'ogg';
        else if (mimeType.includes('wav')) extension = 'wav';
        
        // Create the audio file with the correct extension
        const audioFile = new File([audioBlob], `recording.${extension}`, { type: mimeType });
        
        console.log('Recording saved:', {
          name: audioFile.name,
          type: audioFile.type,
          size: audioFile.size,
          extension: extension,
          mimeType: mimeType,
          blobSize: audioBlob.size,
          chunksCount: recordedChunksRef.current.length
        });
        
        // Validate file size (ensure it's not empty)
        if (audioFile.size === 0) {
          console.error('File size is 0');
          setError('Recording failed - no audio data captured. Please try again.');
          setIsRecording(false);
          setRecordingTime(0);
          stream.getTracks().forEach(track => track.stop());
          return;
        }
        
        setAudioFile(audioFile);
        setRecordedChunks([]);
        recordedChunksRef.current = []; // Clear the ref
        setIsRecording(false);
        setRecordingTime(0);
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop());
      };

      recorder.onerror = (event) => {
        console.error('MediaRecorder error:', event);
        setError('Recording error occurred. Please try again.');
        setIsRecording(false);
        setRecordingTime(0);
        stream.getTracks().forEach(track => track.stop());
      };

      setMediaRecorder(recorder);
      
      // Try different recording approaches
      let recordingStarted = false;
      
      // Approach 1: Try with timeslice
      try {
        console.log('Trying recording with timeslice...');
        recorder.start(1000); // Capture data every 1 second
        recordingStarted = true;
      } catch (error) {
        console.warn('Failed to start with timeslice:', error);
        
        // Approach 2: Try without timeslice
        try {
          console.log('Trying recording without timeslice...');
          recorder.start();
          recordingStarted = true;
        } catch (fallbackError) {
          console.error('Failed to start recorder even without timeslice:', fallbackError);
          
          // Approach 3: Try with a very small timeslice
          try {
            console.log('Trying recording with small timeslice...');
            recorder.start(100); // 100ms timeslice
            recordingStarted = true;
          } catch (finalError) {
            console.error('All recording approaches failed:', finalError);
            
            // Approach 4: Try with no options at all
            try {
              console.log('Trying recording with no options...');
              recorder.start();
              recordingStarted = true;
            } catch (lastError) {
              console.error('All MediaRecorder approaches failed:', lastError);
              setError('Failed to start recording. Please try refreshing the page or use a different browser.');
              stream.getTracks().forEach(track => track.stop());
              return;
            }
          }
        }
      }
      
      if (!recordingStarted) {
        setError('Failed to start recording. Please try again.');
        stream.getTracks().forEach(track => track.stop());
      }
      
    } catch (err) {
      console.error('Recording error:', err);
      setError('Failed to access microphone. Please ensure microphone permissions are granted.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      console.log('Stopping recording...');
      
      try {
        // Request data before stopping to ensure we get any pending data
        mediaRecorder.requestData();
        
        // Stop the recorder
        mediaRecorder.stop();
        
        console.log('Recording stop requested');
      } catch (error) {
        console.error('Error stopping recording:', error);
        setError('Error stopping recording. Please try again.');
        
        // Force cleanup
        if (recordingTimerRef.current) {
          clearInterval(recordingTimerRef.current);
          recordingTimerRef.current = null;
        }
        setIsRecording(false);
        setRecordingTime(0);
      }
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!audioFile) return;

    setIsProcessing(true);
    setError('');
    setResult(null);

    console.log('Submitting audio file:', {
      name: audioFile.name,
      type: audioFile.type,
      size: audioFile.size,
      lastModified: audioFile.lastModified
    });

    // Validate file format before sending
    const supportedExtensions = ['.mp3', '.wav', '.m4a', '.flac', '.webm', '.mp4', '.ogg', '.aac'];
    const fileExtension = '.' + audioFile.name.split('.').pop()?.toLowerCase();
    
    if (!supportedExtensions.includes(fileExtension)) {
      setError(`Unsupported file format: ${fileExtension}. Supported formats: ${supportedExtensions.join(', ')}`);
      setIsProcessing(false);
      return;
    }

    // Validate file size
    if (audioFile.size === 0) {
      setError('Audio file is empty. Please record again.');
      setIsProcessing(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append('audio_file', audioFile);

      console.log('Sending request to backend...');
      const response = await fetch('http://localhost:8000/speech-to-text', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      console.log('Backend response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Backend error response:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json();
      console.log('Backend success response:', data);
      setResult(data);
    } catch (err) {
      console.error('Speech-to-text error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred during transcription');
    } finally {
      setIsProcessing(false);
    }
  };

  const handlePlayAudio = () => {
    if (!audioFile) return;

    if (isPlaying && audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
      return;
    }

    // Create a new blob URL for each play to avoid caching issues
    const blobUrl = URL.createObjectURL(audioFile);
    console.log('Playing audio file:', audioFile.name, 'Type:', audioFile.type, 'Size:', audioFile.size);
    
    const audio = new Audio();
    
    // Set audio properties for better compatibility
    audio.preload = 'metadata';
    audio.crossOrigin = 'anonymous';
    
    // Add event listeners before setting src
    audio.addEventListener('ended', () => {
      setIsPlaying(false);
      URL.revokeObjectURL(blobUrl); // Clean up the blob URL
    });
    
    audio.addEventListener('error', (e) => {
      console.error('Audio playback error:', e);
      console.error('Audio error details:', audio.error);
      setError(`Error playing audio file: ${audio.error?.message || 'Unknown error'}. The audio format may not be supported by your browser.`);
      setIsPlaying(false);
      URL.revokeObjectURL(blobUrl);
    });

    audio.addEventListener('canplaythrough', () => {
      audioRef.current = audio;
      setIsPlaying(true);
      audio.play().catch(err => {
        console.error('Failed to play audio:', err);
        setError(`Failed to play audio file: ${err.message}. Please try a different audio format.`);
        setIsPlaying(false);
        URL.revokeObjectURL(blobUrl);
      });
    });

    audio.addEventListener('loadstart', () => {
      console.log('Audio loading started');
    });

    audio.addEventListener('loadedmetadata', () => {
      console.log('Audio metadata loaded, duration:', audio.duration);
    });

    // Add timeout for loading
    const loadTimeout = setTimeout(() => {
      if (!audio.readyState || audio.readyState < 2) {
        setError('Audio file took too long to load. Please try a different file.');
        URL.revokeObjectURL(blobUrl);
      }
    }, 15000); // 15 second timeout

    audio.addEventListener('canplay', () => {
      clearTimeout(loadTimeout);
      console.log('Audio can play');
    });

    // Set the source after adding all event listeners
    audio.src = blobUrl;
  };

  const handleDownloadTranscript = () => {
    if (result) {
      const blob = new Blob([result.transcript], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'transcript.txt';
      link.click();
      URL.revokeObjectURL(url);
    }
  };

  // Cleanup function for recording timer
  const cleanupRecording = () => {
    if (recordingTimerRef.current) {
      clearInterval(recordingTimerRef.current);
      recordingTimerRef.current = null;
    }
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  // Cleanup on component unmount
  React.useEffect(() => {
    return () => {
      cleanupRecording();
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  const clearRecording = () => {
    setAudioFile(null);
    setRecordedChunks([]);
    recordedChunksRef.current = []; // Clear the ref
    setError('');
    setResult(null);
    setIsPlaying(false);
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
  };

  return (
    <div className="p-8">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center justify-center">
          <Mic className="mr-3 h-8 w-8 text-blue-600" />
          Speech to Text
        </h2>
        <p className="text-gray-600">
          Upload an audio file or record your voice to convert speech to text
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Live Recording Section */}
        <div className="mb-6 p-4 border border-gray-300 rounded-lg bg-gray-50">
          <h3 className="text-lg font-semibold mb-3 text-gray-800">Live Recording</h3>
          
          <div className="flex flex-wrap gap-3 mb-4">
            {!isRecording ? (
              <button
                onClick={startRecording}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
              >
                <Square className="w-4 h-4" />
                Start Recording
              </button>
            ) : (
              <button
                onClick={stopRecording}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors flex items-center gap-2"
              >
                <Square className="w-4 h-4" />
                Stop Recording
              </button>
            )}
            
            {isRecording && (
              <div className="flex items-center gap-2 text-red-600">
                <div className="w-2 h-2 bg-red-600 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Recording... {formatTime(recordingTime)}</span>
              </div>
            )}
            
            {audioFile && (
              <button
                onClick={clearRecording}
                className="px-3 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors text-sm"
              >
                Clear Recording
              </button>
            )}
          </div>
          
          {/* Test Recording Button */}
          <div className="mb-3">
            <button
              onClick={async () => {
                console.log('=== TEST RECORDING ===');
                console.log('MediaRecorder supported:', !!window.MediaRecorder);
                console.log('getUserMedia supported:', !!navigator.mediaDevices?.getUserMedia);
                console.log('AudioContext supported:', !!window.AudioContext);
                console.log('User agent:', navigator.userAgent);
                console.log('Platform:', navigator.platform);
                console.log('Browser:', navigator.appName);
                console.log('Version:', navigator.appVersion);
                
                try {
                  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                  console.log('Test stream obtained:', stream.getAudioTracks().length, 'tracks');
                  console.log('Track settings:', stream.getAudioTracks()[0]?.getSettings());
                  
                  // Test MediaRecorder creation
                  try {
                    const testRecorder = new MediaRecorder(stream);
                    console.log('Test MediaRecorder created successfully');
                    console.log('Supported MIME types:');
                    ['audio/webm', 'audio/mp4', 'audio/ogg', 'audio/wav'].forEach(type => {
                      console.log(`  ${type}: ${MediaRecorder.isTypeSupported(type)}`);
                    });
                    
                    // Test recording start
                    testRecorder.start();
                    console.log('Test recording started');
                    
                    // Stop after a short time
                    setTimeout(() => {
                      testRecorder.stop();
                      console.log('Test recording stopped');
                    }, 1000);
                    
                  } catch (recorderError) {
                    console.error('Test MediaRecorder failed:', recorderError);
                  }
                  
                  stream.getTracks().forEach(track => track.stop());
                } catch (err) {
                  console.error('Test getUserMedia failed:', err);
                }
              }}
              className="px-3 py-1 bg-blue-500 text-white rounded text-xs hover:bg-blue-600 transition-colors"
            >
              Test Microphone
            </button>
            
            {/* Debug Info Display */}
            <div className="mt-2 text-xs text-gray-600">
              <details>
                <summary className="cursor-pointer text-blue-600">Browser Info</summary>
                <div className="mt-1 p-2 bg-gray-100 rounded text-xs">
                  <div>User Agent: {navigator.userAgent}</div>
                  <div>Platform: {navigator.platform}</div>
                  <div>MediaRecorder: {window.MediaRecorder ? '✅ Supported' : '❌ Not Supported'}</div>
                  <div>getUserMedia: {navigator.mediaDevices ? '✅ Supported' : '❌ Not Supported'}</div>
                </div>
              </details>
            </div>
          </div>
          
          {audioFile && !isRecording && (
            <div className="text-sm text-gray-600 bg-green-50 p-3 rounded-lg border border-green-200">
              <div className="font-medium text-green-800">Recording saved!</div>
              <div className="text-green-700">File: {audioFile.name}</div>
              <div className="text-green-700">Size: {audioFile.size ? (audioFile.size / 1024).toFixed(1) : 'N/A'} KB</div>
              <div className="text-green-700">Type: {audioFile.type}</div>
              <div className="text-green-700">Extension: .{audioFile.name.split('.').pop()}</div>
              <div className="text-green-700">Click "Convert to Text" below to process.</div>
              
              {/* Debug info */}
              <details className="mt-2">
                <summary className="text-green-600 cursor-pointer text-xs">Debug Info</summary>
                <div className="mt-1 text-xs text-green-600 bg-green-100 p-2 rounded">
                  <div>MIME Type: {audioFile.type}</div>
                  <div>File Size: {audioFile.size} bytes</div>
                  <div>Last Modified: {new Date(audioFile.lastModified).toLocaleString()}</div>
                  <div>Supported by Backend: {['.mp3', '.wav', '.m4a', '.flac', '.webm', '.mp4', '.ogg', '.aac'].includes('.' + audioFile.name.split('.').pop()?.toLowerCase()) ? '✅ Yes' : '❌ No'}</div>
                </div>
              </details>
            </div>
          )}
        </div>

        {/* File Upload Section */}
        <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg p-6 border border-green-200">
          <h3 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <Upload className="mr-2 h-5 w-5 text-green-600" />
            Upload Audio File
          </h3>
          
          <div className="space-y-4">
            <input
              type="file"
              accept="audio/*"
              onChange={handleFileChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              disabled={isProcessing}
            />
            
            {audioFile && (
              <div className="text-sm text-gray-600">
                File selected: {audioFile.name}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Audio Preview and Controls */}
      {audioFile && (
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Audio Preview</h3>
          
          <div className="flex items-center space-x-4 mb-4">
            <button
              onClick={handlePlayAudio}
              disabled={isProcessing}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 disabled:opacity-50"
            >
              {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              {isPlaying ? ' Pause' : ' Play'}
            </button>
            
            <button
              onClick={clearRecording}
              className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
            >
              Clear
            </button>
          </div>
          
          <div className="text-sm text-gray-600">
            File: {audioFile.name} | Type: {audioFile.type || 'audio/wav'}
          </div>
        </div>
      )}

      {/* Convert to Text Button */}
      {audioFile && (
        <form onSubmit={handleSubmit} className="text-center mb-6">
          <button
            type="submit"
            disabled={isProcessing}
            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-medium py-3 px-8 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center mx-auto"
          >
            {isProcessing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Converting to Text...
              </>
            ) : (
              'Convert to Text'
            )}
          </button>
          
          {isProcessing && (
            <div className="mt-3 text-sm text-gray-600">
              Processing audio... This may take a few moments depending on the file size.
            </div>
          )}
        </form>
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold text-gray-800">Transcription Result</h3>
            <button
              onClick={handleDownloadTranscript}
              className="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200 flex items-center"
            >
              <Download className="mr-2 h-4 w-4" />
              Download
            </button>
          </div>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Transcript</h4>
              <div className="p-4 bg-gray-50 rounded-lg border text-gray-800">
                {result.transcript}
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {result.confidence ? result.confidence.toFixed(1) : 'N/A'}%
                </div>
                <div className="text-sm text-gray-600">Confidence</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {result.processing_time ? result.processing_time.toFixed(2) : 'N/A'}s
                </div>
                <div className="text-sm text-gray-600">Processing Time</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {result.transcript ? result.transcript.split(' ').length : 0}
                </div>
                <div className="text-sm text-gray-600">Word Count</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SpeechToText;
