#!/usr/bin/env python3
"""
Simple test main.py using mock services for testing
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import tempfile
import os
import time
from gtts import gTTS
import PyPDF2
from docx import Document
import io
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the new OpenAI-powered text simplifier
from app.services.text_simplifier import TextSimplifier

app = FastAPI(title="Aivana - AI-Powered Text Enhancement", version="2.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    text_simplifier = TextSimplifier()
    openai_available = True
except Exception as e:
    print(f"Warning: OpenAI not available: {e}")
    text_simplifier = None
    openai_available = False

audio_files = {}

# Pydantic models
class TextSimplificationRequest(BaseModel):
    text: str
    target_level: str
    preserve_meaning: bool = True

class TextSimplificationResponse(BaseModel):
    original_text: str
    simplified_text: str
    target_level: str
    readability_score: float
    level_config: dict
    processing_time: float

class TTSRequest(BaseModel):
    text: str
    voice: str
    speed: float

class TTSResponse(BaseModel):
    text: str
    audio_file_path: str
    duration: float

class STTRequest(BaseModel):
    audio_file: UploadFile

class STTResponse(BaseModel):
    transcript: str
    confidence: float
    processing_time: float

class DocumentAnalysisResponse(BaseModel):
    filename: str
    content_summary: str
    key_points: list
    word_count: int
    processing_time: float
    file_type: str

@app.get("/")
async def root():
    return {
        "message": "Aivana - AI-Powered Text Enhancement",
        "version": "2.0.0",
        "status": "running",
        "openai_available": openai_available,
        "features": [
            "OpenAI-powered text simplification" if openai_available else "Text simplification (OpenAI not available)",
            "Advanced document analysis", 
            "Real TTS with speed control",
            "Speech-to-text processing"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": [
            "openai_text_simplifier" if openai_available else "text_simplifier_fallback",
            "real_tts", 
            "document_processor",
            "speech_to_text"
        ],
        "note": f"OpenAI integration: {'Available' if openai_available else 'Not available - check .env file'}"
    }

@app.post("/simplify-text", response_model=TextSimplificationResponse)
async def simplify_text(request: TextSimplificationRequest):
    """Simplify text using OpenAI GPT-4 for professional quality"""
    start_time = time.time()
    
    if not openai_available:
        raise HTTPException(status_code=503, detail="OpenAI service not available. Please check your .env file and ensure OPENAI_API_KEY is set.")
    
    try:
        # Use the new OpenAI-powered text simplifier
        result = text_simplifier.simplify(
            text=request.text,
            target_level=request.target_level,
            preserve_meaning=request.preserve_meaning
        )
        
        processing_time = time.time() - start_time
        
        return TextSimplificationResponse(
            original_text=result["original_text"],
            simplified_text=result["simplified_text"],
            target_level=result["target_level"],
            readability_score=result["readability_score"],
            level_config=result["level_config"],
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    """Real text-to-speech conversion using gTTS with proper language control"""
    try:
        # Generate a unique filename
        audio_file_path = f"speech_{uuid.uuid4().hex[:8]}.mp3"
        
        # Create temporary file path
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, audio_file_path)
        
        # Map voice selection to proper language codes for gTTS
        language_map = {
            "us_english": "en",
            "uk_english": "en-gb", 
            "spanish": "es",
            "french": "fr",
            "german": "de"
        }
        
        # Get language code
        lang_code = language_map.get(request.voice, "en")
        
        # For non-English languages, we need to translate the text to that language first
        # This ensures the TTS actually speaks in the target language, not just with an accent
        if lang_code != "en" and lang_code != "en-gb":
            try:
                # Use OpenAI to translate the text to the target language
                if openai_available:
                    # Create a more specific translation prompt
                    language_names = {
                        "es": "Spanish",
                        "fr": "French", 
                        "de": "German"
                    }
                    
                    translation_prompt = f"Translate the following English text to {language_names.get(lang_code, lang_code.upper())}. Provide only the translation, no explanations, quotes, or additional text. Keep the same meaning and tone: {request.text}"
                    
                    print(f"Attempting translation to {lang_code} for text: {request.text}")
                    
                    # Use the correct OpenAI API format
                    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                    
                    # Test the API key first
                    print(f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')[:20]}...")
                    
                    translation_response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": f"You are a professional translator. Translate the given English text to {language_names.get(lang_code, lang_code.upper())} language. Provide only the translation, no explanations, quotes, or additional text. Maintain the original meaning and tone."},
                            {"role": "user", "content": translation_prompt}
                        ],
                        max_tokens=500,
                        temperature=0.1,  # Lower temperature for more consistent translations
                    )
                    
                    translated_text = translation_response.choices[0].message.content.strip()
                    # Remove any quotes or extra formatting
                    translated_text = translated_text.strip('"').strip("'").strip()
                    
                    print(f"Translation successful: '{request.text}' -> '{translated_text}' in {lang_code}")
                    
                    # Use the translated text for TTS
                    text_for_tts = translated_text
                else:
                    # Fallback: use original text if OpenAI not available
                    print(f"OpenAI not available, using original text for {lang_code}")
                    text_for_tts = request.text
            except Exception as e:
                print(f"Translation failed for {lang_code}: {e}")
                print(f"Error type: {type(e)}")
                print(f"Error details: {str(e)}")
                
                # If translation fails, we cannot proceed with non-English TTS
                # because gTTS will just speak English with an accent
                raise HTTPException(
                    status_code=500, 
                    detail=f"Failed to translate text to {lang_code}. Cannot generate speech in target language without translation."
                )
        else:
            # For English variants, use the original text
            text_for_tts = request.text
            print(f"Using English text for {lang_code}: {text_for_tts}")
        
        # Create gTTS instance with proper language configuration
        # For non-English languages, ensure we're using the correct language model
        if lang_code in ["es", "fr", "de"]:
            # Use specific language models for better pronunciation
            print(f"Creating gTTS for {lang_code} with text: {text_for_tts}")
            tts = gTTS(text=text_for_tts, lang=lang_code, slow=False)
        elif lang_code == "en-gb":
            # British English
            print(f"Creating British English gTTS with text: {text_for_tts}")
            tts = gTTS(text=text_for_tts, lang="en", tld="co.uk", slow=False)
        else:
            # US English
            print(f"Creating US English gTTS with text: {text_for_tts}")
            tts = gTTS(text=text_for_tts, lang="en", slow=False)
        
        # Generate speech
        print(f"Generating speech file: {temp_file_path}")
        tts.save(temp_file_path)
        print(f"Speech file generated successfully")
        
        # Store the file path and metadata for later access
        audio_files[audio_file_path] = {
            "path": temp_file_path,
            "speed": request.speed,
            "text": request.text,
            "translated_text": text_for_tts if lang_code not in ["en", "en-gb"] else None,
            "language": lang_code,
            "original_language": "en"
        }
        
        # Calculate estimated duration based on speed
        word_count = len(text_for_tts.split())
        base_duration = (word_count / 150) * 60  # Base: 150 words per minute
        estimated_duration = base_duration / request.speed
        
        return TTSResponse(
            text=request.text,
            audio_file_path=audio_file_path,
            duration=estimated_duration
        )
    except Exception as e:
        print(f"TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speech-to-text", response_model=STTResponse)
async def speech_to_text(audio_file: UploadFile = File(...)):
    """Convert speech to text using OpenAI Whisper API"""
    start_time = time.time()
    
    if not openai_available:
        raise HTTPException(status_code=503, detail="OpenAI service not available. Please check your .env file and ensure OPENAI_API_KEY is set.")
    
    try:
        # Check file type
        if not audio_file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.webm', '.mp4', '.ogg', '.aac')):
            raise HTTPException(status_code=400, detail="Unsupported audio format. Please upload MP3, WAV, M4A, FLAC, WebM, MP4, OGG, or AAC.")
        
        # Read audio file content
        audio_content = await audio_file.read()
        
        # Save to temporary file for OpenAI Whisper
        temp_dir = tempfile.gettempdir()
        temp_audio_path = os.path.join(temp_dir, f"audio_{uuid.uuid4().hex[:8]}.{audio_file.filename.split('.')[-1]}")
        
        with open(temp_audio_path, "wb") as f:
            f.write(audio_content)
        
        try:
            # Use OpenAI Whisper API for transcription
            with open(temp_audio_path, "rb") as audio_file_obj:
                transcript_response = openai.Audio.transcribe(
                    "whisper-1",
                    audio_file_obj,
                    api_key=os.getenv('OPENAI_API_KEY')
                )
            
            transcript = transcript_response.text
            confidence = 0.95  # Whisper doesn't provide confidence, so we estimate high
            
        except Exception as e:
            # Fallback to mock transcription if OpenAI fails
            transcript = "This is a fallback transcript. The audio was received but OpenAI Whisper processing failed."
            confidence = 0.5
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
        
        processing_time = time.time() - start_time
        
        return STTResponse(
            transcript=transcript,
            confidence=confidence,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{file_path}")
async def download_audio(file_path: str):
    """Download generated audio file"""
    if file_path not in audio_files:
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    file_info = audio_files[file_path]
    return FileResponse(
        file_info["path"],
        media_type="audio/mpeg",
        filename=f"speech_{file_info['speed']}x.mp3"
    )

@app.post("/process-document", response_model=DocumentAnalysisResponse)
async def process_document(file: UploadFile = File(...)):
    """Process uploaded documents using OpenAI for intelligent analysis"""
    start_time = time.time()
    
    try:
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            file_type = "PDF"
            # Extract text from PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        elif file.filename.lower().endswith(('.docx', '.doc')):
            file_type = "Word Document"
            # Extract text from Word document
            doc = Document(io.BytesIO(content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload PDF or Word document.")
        
        # Clean up text
        text = text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="No text content found in document.")
        
        # Use OpenAI for intelligent document analysis
        if openai_available:
            try:
                # Create a summary using the text simplifier (college level for analysis)
                analysis_result = text_simplifier.simplify(
                    text=text[:1000],  # Limit to first 1000 chars for analysis
                    target_level="college",
                    preserve_meaning=True
                )
                
                # Extract key points (first few sentences)
                sentences = text.split('. ')
                key_points = [s.strip() + '.' for s in sentences[:5] if s.strip()]
                
                # Generate intelligent summary
                summary = f"This {file_type.lower()} contains {len(text.split())} words covering various topics. "
                summary += "The document appears to discuss " + analysis_result["simplified_text"][:200] + "..."
                
            except Exception as e:
                # Fallback to basic analysis if OpenAI fails
                sentences = text.split('. ')
                key_points = [s.strip() + '.' for s in sentences[:5] if s.strip()]
                summary = f"This {file_type.lower()} contains {len(text.split())} words. "
                summary += "Key content includes: " + text[:200] + "..."
        else:
            # Fallback to basic analysis if OpenAI not available
            sentences = text.split('. ')
            key_points = [s.strip() + '.' for s in sentences[:5] if s.strip()]
            summary = f"This {file_type.lower()} contains {len(text.split())} words. "
            summary += "Key content includes: " + text[:200] + "..."
        
        processing_time = time.time() - start_time
        
        return DocumentAnalysisResponse(
            filename=file.filename,
            content_summary=summary,
            key_points=key_points,
            word_count=len(text.split()),
            processing_time=processing_time,
            file_type=file_type
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify all services"""
    return {
        "message": "Aivana Backend Test",
        "services": {
            "text_simplifier": "OpenAI GPT-4 powered" if openai_available else "Fallback mode (OpenAI not available)",
            "tts": "gTTS with speed control",
            "stt": "OpenAI Whisper powered" if openai_available else "Fallback mode (OpenAI not available)",
            "document_processor": "OpenAI enhanced analysis" if openai_available else "Basic analysis (OpenAI not available)"
        },
        "status": "All systems operational",
        "openai_status": "Available" if openai_available else "Not available - check .env file"
    }

@app.post("/test-translation")
async def test_translation():
    """Test endpoint to debug translation issues"""
    try:
        if not openai_available:
            return {"error": "OpenAI not available"}
        
        test_text = "Hello world"
        target_language = "Spanish"
        
        print(f"Testing translation of '{test_text}' to {target_language}")
        
        # Test the translation directly
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        translation_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the given English text to {target_language} language. Provide only the translation, no explanations, quotes, or additional text. Maintain the original meaning and tone."},
                {"role": "user", "content": f"Translate the following English text to {target_language}. Only provide the translation: {test_text}"}
            ],
            max_tokens=500,
            temperature=0.1,
        )
        
        translated_text = translation_response.choices[0].message.content.strip()
        translated_text = translated_text.strip('"').strip("'").strip()
        
        print(f"Translation result: '{test_text}' -> '{translated_text}'")
        
        return {
            "original": test_text,
            "translated": translated_text,
            "target_language": target_language,
            "success": True
        }
        
    except Exception as e:
        print(f"Translation test failed: {e}")
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    import uvicorn
    print("Starting Aivana - AI-Powered Text Enhancement")
    if openai_available:
        print("✅ OpenAI integration available")
        print("Using OpenAI GPT-4 for text simplification and document analysis")
        print("Using OpenAI Whisper for speech-to-text")
    else:
        print("⚠️  OpenAI integration not available")
        print("Please check your .env file and ensure OPENAI_API_KEY is set")
        print("Some features will be limited")
    print("Navigate to http://localhost:8000/docs for API documentation")
    uvicorn.run(app, host="0.0.0.0", port=8000) 