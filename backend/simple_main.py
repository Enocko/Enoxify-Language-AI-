from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
import asyncio
import json
from typing import Optional
from pydantic import BaseModel

# Simple request/response models
class TextSimplificationRequest(BaseModel):
    text: str
    target_level: str = "simple"
    preserve_meaning: bool = True

class TextSimplificationResponse(BaseModel):
    original_text: str
    simplified_text: str
    readability_score: float
    processing_time: float

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "en-US"
    speed: float = 1.0

class TextToSpeechResponse(BaseModel):
    text: str
    audio_file: str
    duration: float
    processing_time: float

class SpeechToTextResponse(BaseModel):
    transcript: str
    confidence: float
    processing_time: float

class DocumentProcessingRequest(BaseModel):
    content: str
    output_formats: list[str]

class DocumentProcessingResponse(BaseModel):
    original_format: str
    output_formats: list[str]
    processing_time: float
    simplified_text: Optional[str] = None
    audio_file: Optional[str] = None

# Create FastAPI app
app = FastAPI(
    title="AI-Based Accessibility Enhancer (Demo)",
    description="Convert educational content into accessible formats",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock services for demo purposes
class MockTextSimplifier:
    async def simplify(self, text: str, target_level: str, preserve_meaning: bool) -> str:
        await asyncio.sleep(1)  # Simulate processing time
        
        # Simple text simplification logic
        if target_level == "simple":
            # Replace complex words with simpler ones
            replacements = {
                "utilize": "use",
                "implement": "put into action",
                "facilitate": "help",
                "methodology": "method",
                "comprehensive": "complete",
                "sophisticated": "advanced",
                "optimize": "improve",
                "leverage": "use",
                "paradigm": "pattern",
                "synergy": "working together"
            }
            
            simplified = text
            for complex_word, simple_word in replacements.items():
                simplified = simplified.replace(complex_word, simple_word)
            
            return simplified
        return text
    
    def calculate_readability(self, text: str) -> float:
        # Simple readability calculation
        words = text.split()
        sentences = text.split('.')
        syllables = sum(len(word) // 3 for word in words)
        
        if len(words) == 0 or len(sentences) == 0:
            return 0.0
        
        # Flesch Reading Ease formula (simplified)
        score = 206.835 - (1.015 * (len(words) / len(sentences))) - (84.6 * (syllables / len(words)))
        return max(0.0, min(100.0, score))

class MockTextToSpeech:
    async def convert(self, text: str, voice: str, speed: float) -> str:
        await asyncio.sleep(1.5)  # Simulate processing time
        return f"mock_audio_{hash(text) % 10000}.mp3"
    
    def get_audio_duration(self, text: str) -> float:
        # Estimate duration based on text length
        words = len(text.split())
        return words * 0.5  # Rough estimate: 0.5 seconds per word

class MockSpeechToText:
    async def transcribe(self, audio_file: UploadFile) -> dict:
        await asyncio.sleep(2)  # Simulate processing time
        
        # Mock transcription
        mock_transcript = "This is a demonstration of speech recognition technology. The system can convert spoken words into written text with high accuracy."
        
        return {
            "transcript": mock_transcript,
            "confidence": 0.94,
            "word_timestamps": [
                {"word": "This", "start": 0.0, "end": 0.5, "confidence": 0.95},
                {"word": "is", "start": 0.5, "end": 0.8, "confidence": 0.98},
                {"word": "a", "start": 0.8, "end": 1.0, "confidence": 0.99},
                {"word": "demonstration", "start": 1.0, "end": 2.5, "confidence": 0.92},
                {"word": "of", "start": 2.5, "end": 2.8, "confidence": 0.97},
                {"word": "speech", "start": 2.8, "end": 3.2, "confidence": 0.94},
                {"word": "recognition", "start": 3.2, "end": 4.0, "confidence": 0.91},
                {"word": "technology", "start": 4.0, "end": 5.0, "confidence": 0.93}
            ]
        }

class MockDocumentProcessor:
    async def process(self, content: str, output_formats: list[str]) -> dict:
        await asyncio.sleep(2)  # Simulate processing time
        
        result = {
            "original_format": "text",
            "output_formats": output_formats,
            "processing_time": 2.0
        }
        
        if "simplified_text" in output_formats:
            result["simplified_text"] = "This is a simplified version of your document content. The AI has processed your document and made it more accessible."
        
        if "audio" in output_formats:
            result["audio_file"] = f"mock_audio_{hash(content) % 10000}.mp3"
        
        return result

# Initialize mock services
text_simplifier = MockTextSimplifier()
text_to_speech = MockTextToSpeech()
speech_to_text = MockSpeechToText()
document_processor = MockDocumentProcessor()

@app.get("/")
async def root():
    return {"message": "AI-Based Accessibility Enhancer API (Demo Mode)"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "services": ["text_simplifier", "speech_to_text", "text_to_speech", "document_processor"],
        "mode": "demo"
    }

@app.post("/simplify-text", response_model=TextSimplificationResponse)
async def simplify_text(request: TextSimplificationRequest):
    start_time = asyncio.get_event_loop().time()
    
    try:
        simplified_text = await text_simplifier.simplify(
            request.text, 
            request.target_level, 
            request.preserve_meaning
        )
        
        readability_score = text_simplifier.calculate_readability(simplified_text)
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return TextSimplificationResponse(
            original_text=request.text,
            simplified_text=simplified_text,
            readability_score=readability_score,
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text simplification failed: {str(e)}")

@app.post("/text-to-speech", response_model=TextToSpeechResponse)
async def convert_text_to_speech(request: TextToSpeechRequest):
    start_time = asyncio.get_event_loop().time()
    
    try:
        audio_file = await text_to_speech.convert(
            request.text, 
            request.voice, 
            request.speed
        )
        duration = text_to_speech.get_audio_duration(request.text)
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return TextToSpeechResponse(
            text=request.text,
            audio_file=audio_file,
            duration=duration,
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}")

@app.post("/speech-to-text", response_model=SpeechToTextResponse)
async def convert_speech_to_text(audio_file: UploadFile = File(...)):
    start_time = asyncio.get_event_loop().time()
    
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        result = await speech_to_text.transcribe(audio_file)
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return SpeechToTextResponse(
            transcript=result["transcript"],
            confidence=result["confidence"],
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}")

@app.post("/process-document", response_model=DocumentProcessingResponse)
async def process_document(request: DocumentProcessingRequest):
    start_time = asyncio.get_event_loop().time()
    
    try:
        result = await document_processor.process(
            request.content, 
            request.output_formats
        )
        
        return DocumentProcessingResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting AI-Based Accessibility Enhancer (Demo Mode)")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("🔧 This is a demo version with mock AI services")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
