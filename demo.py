#!/usr/bin/env python3
"""
Demo script for the AI-Based Accessibility Enhancer
This script demonstrates the core functionality without requiring external API keys
"""

import asyncio
import time
from typing import Dict, Any

class MockTextSimplifier:
    """Mock text simplifier for demonstration purposes"""
    
    def __init__(self):
        self.simplification_examples = {
            "The quantum mechanical properties of subatomic particles exhibit wave-particle duality, a fundamental principle that challenges classical physics paradigms.": 
            "Tiny particles act like both waves and particles at the same time. This is a basic rule that goes against old physics ideas.",
            
            "The implementation of machine learning algorithms necessitates comprehensive data preprocessing, feature engineering, and hyperparameter optimization to achieve optimal performance metrics.":
            "To use machine learning, you need to clean your data, create good features, and adjust settings to get the best results.",
            
            "Neuroscientific research indicates that cognitive processes are mediated by complex neural networks involving multiple brain regions and neurotransmitter systems.":
            "Brain research shows that thinking happens through networks of brain cells that work together in different parts of the brain."
        }
    
    async def simplify(self, text: str, target_level: str = "middle_school", preserve_meaning: bool = True) -> str:
        """Mock text simplification"""
        await asyncio.sleep(1)  # Simulate processing time
        
        # Find the best match in our examples
        for complex_text, simple_text in self.simplification_examples.items():
            if complex_text.lower() in text.lower() or text.lower() in complex_text.lower():
                return simple_text
        
        # If no match found, return a generic simplification
        return f"Simplified version of: {text[:100]}..."
    
    def calculate_readability(self, text: str) -> float:
        """Calculate mock readability score"""
        words = len(text.split())
        sentences = text.count('.') + text.count('!') + text.count('?')
        if sentences == 0:
            sentences = 1
        
        # Simple formula: shorter sentences and words = higher score
        avg_sentence_length = words / sentences
        score = max(20, min(95, 100 - (avg_sentence_length * 2)))
        return round(score, 1)

class MockTextToSpeech:
    """Mock text-to-speech service"""
    
    async def convert(self, text: str, voice: str = "neutral", speed: float = 1.0, language: str = "en-US") -> str:
        """Mock TTS conversion"""
        await asyncio.sleep(2)  # Simulate processing time
        return f"mock_audio_{int(time.time())}.mp3"
    
    def get_audio_duration(self, audio_file_path: str) -> float:
        """Mock audio duration calculation"""
        return 15.5  # Mock duration in seconds

class MockSpeechToText:
    """Mock speech-to-text service"""
    
    async def transcribe(self, audio_file, language: str = "en-US", include_timestamps: bool = True) -> Dict[str, Any]:
        """Mock transcription"""
        await asyncio.sleep(2)  # Simulate processing time
        
        mock_transcript = "This is a demonstration of speech recognition technology. The system can convert spoken words into written text with high accuracy."
        
        timestamps = [
            {"word": "This", "start": 0.0, "end": 0.5, "confidence": 0.95},
            {"word": "is", "start": 0.5, "end": 0.8, "confidence": 0.98},
            {"word": "a", "start": 0.8, "end": 1.0, "confidence": 0.99},
            {"word": "demonstration", "start": 1.0, "end": 2.5, "confidence": 0.92},
            {"word": "of", "start": 2.5, "end": 2.8, "confidence": 0.97},
            {"word": "speech", "start": 2.8, "end": 3.2, "confidence": 0.94},
            {"word": "recognition", "start": 3.2, "end": 4.0, "confidence": 0.91},
            {"word": "technology", "start": 4.0, "end": 5.0, "confidence": 0.93}
        ]
        
        return {
            "transcript": mock_transcript,
            "timestamps": timestamps,
            "confidence": 0.94
        }

class MockDocumentProcessor:
    """Mock document processor"""
    
    async def process(self, file_path: str, output_format: str = "both", 
                     include_audio: bool = True, include_simplified_text: bool = True) -> Dict[str, Any]:
        """Mock document processing"""
        await asyncio.sleep(3)  # Simulate processing time
        
        return {
            "original_format": "PDF",
            "output_formats": ["simplified_text", "audio"] if include_audio and include_simplified_text else 
                             ["audio"] if include_audio else ["simplified_text"],
            "simplified_text": "This is a simplified version of your document content. The AI has processed your document and made it more accessible by breaking down complex language into simpler terms while preserving the original meaning." if include_simplified_text else None,
            "audio_file_path": f"mock_audio_{int(time.time())}.mp3" if include_audio else None,
            "processing_time": 3.2,
            "file_size": 1024000  # 1MB
        }

async def demo_text_simplification():
    """Demonstrate text simplification"""
    print("🔍 Text Simplification Demo")
    print("=" * 50)
    
    simplifier = MockTextSimplifier()
    
    complex_texts = [
        "The quantum mechanical properties of subatomic particles exhibit wave-particle duality, a fundamental principle that challenges classical physics paradigms.",
        "The implementation of machine learning algorithms necessitates comprehensive data preprocessing, feature engineering, and hyperparameter optimization to achieve optimal performance metrics.",
        "Neuroscientific research indicates that cognitive processes are mediated by complex neural networks involving multiple brain regions and neurotransmitter systems."
    ]
    
    for i, text in enumerate(complex_texts, 1):
        print(f"\n📝 Example {i}:")
        print(f"Original: {text}")
        
        simplified = await simplifier.simplify(text, "middle_school", True)
        readability = simplifier.calculate_readability(simplified)
        
        print(f"Simplified: {simplified}")
        print(f"Readability Score: {readability}/100")
        print("-" * 50)

async def demo_text_to_speech():
    """Demonstrate text-to-speech"""
    print("\n🔊 Text-to-Speech Demo")
    print("=" * 50)
    
    tts = MockTextToSpeech()
    
    sample_text = "Welcome to our educational platform. Today we will learn about artificial intelligence and its applications in modern technology."
    
    print(f"Input Text: {sample_text}")
    print("Converting to speech...")
    
    audio_file = await tts.convert(sample_text, "neutral", 1.0, "en-US")
    duration = tts.get_audio_duration(audio_file)
    
    print(f"Audio File: {audio_file}")
    print(f"Duration: {duration} seconds")
    print("-" * 50)

async def demo_speech_to_text():
    """Demonstrate speech-to-text"""
    print("\n🎤 Speech-to-Text Demo")
    print("=" * 50)
    
    stt = MockSpeechToText()
    
    print("Processing audio file...")
    
    # Mock audio file object
    class MockAudioFile:
        def __init__(self):
            self.filename = "demo_audio.wav"
            self.file = None
    
    mock_file = MockAudioFile()
    result = await stt.transcribe(mock_file, "en-US", True)
    
    print(f"Transcript: {result['transcript']}")
    print(f"Confidence: {result['confidence'] * 100:.1f}%")
    print("\nWord-level Timestamps:")
    for timestamp in result['timestamps']:
        print(f"  {timestamp['start']:.1f}s - {timestamp['end']:.1f}s: {timestamp['word']} ({timestamp['confidence']:.2f})")
    print("-" * 50)

async def demo_document_processing():
    """Demonstrate document processing"""
    print("\n📄 Document Processing Demo")
    print("=" * 50)
    
    processor = MockDocumentProcessor()
    
    print("Processing document...")
    
    result = await processor.process("sample_document.pdf", "both", True, True)
    
    print(f"Original Format: {result['original_format']}")
    print(f"Output Formats: {', '.join(result['output_formats'])}")
    print(f"Processing Time: {result['processing_time']} seconds")
    print(f"File Size: {result['file_size'] / 1024 / 1024:.1f} MB")
    
    if result['simplified_text']:
        print(f"\nSimplified Text: {result['simplified_text']}")
    
    if result['audio_file_path']:
        print(f"\nAudio File: {result['audio_file_path']}")
    
    print("-" * 50)

async def main():
    """Run all demos"""
    print("🚀 AI-Based Accessibility Enhancer - Demo Mode")
    print("=" * 60)
    print("This demo shows the core functionality without requiring external API keys.")
    print("In production, you would need OpenAI, Azure, or Google Cloud credentials.\n")
    
    try:
        await demo_text_simplification()
        await demo_text_to_speech()
        await demo_speech_to_text()
        await demo_document_processing()
        
        print("\n✅ Demo completed successfully!")
        print("\n�� Key Features Demonstrated:")
        print("  • Text simplification with readability scoring")
        print("  • Text-to-speech conversion")
        print("  • Speech-to-text transcription with timestamps")
        print("  • Multi-format document processing")
        print("  • Accessibility-focused design")
        
        print("\n🚀 To run the full application:")
        print("  1. Set up your API keys in .env file")
        print("  2. Install dependencies: pip install -r backend/requirements.txt")
        print("  3. Start backend: cd backend && python main.py")
        print("  4. Start frontend: cd frontend && npm install && npm start")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
