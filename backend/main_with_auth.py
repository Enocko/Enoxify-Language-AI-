from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# Import existing services
from app.services.text_simplifier import TextSimplifier
from app.services.speech_to_text import SpeechToText
from app.services.text_to_speech import TextToSpeech
from app.services.document_processor import DocumentProcessor

# Import existing models
from app.models.request_models import (
    TextSimplificationRequest,
    TextToSpeechRequest,
    DocumentProcessingRequest
)
from app.models.response_models import (
    TextSimplificationResponse,
    TextToSpeechResponse,
    SpeechToTextResponse,
    DocumentProcessingResponse
)

# Import authentication components
from app.database import get_db, engine
from app.models.database_models import Base
from app.auth.auth_router import router as auth_router
from app.auth.dependencies import get_current_active_user

import time

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enoxify - AI-Powered Accessibility Platform",
    description="AI-powered platform that makes complex information accessible to everyone",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)

# Initialize services
text_simplifier = TextSimplifier()
speech_to_text = SpeechToText()
text_to_speech = TextToSpeech()
document_processor = DocumentProcessor()

@app.get("/")
async def root():
    return {"message": "Enoxify - AI-Powered Accessibility Platform API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["text_simplifier", "speech_to_text", "text_to_speech", "document_processor"]}

@app.post("/simplify-text", response_model=TextSimplificationResponse)
async def simplify_text(
    request: TextSimplificationRequest,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Simplify complex text into more accessible language"""
    start_time = time.time()
    try:
        result = await text_simplifier.simplify(
            text=request.text,
            target_level=request.target_level,
            preserve_meaning=request.preserve_meaning
        )
        processing_time = time.time() - start_time
        return TextSimplificationResponse(
            original_text=request.text,
            simplified_text=result["simplified_text"],
            readability_score=result["readability_score"],
            processing_time=processing_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech", response_model=TextToSpeechResponse)
async def convert_text_to_speech(
    request: TextToSpeechRequest,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Convert text to natural-sounding speech"""
    try:
        result = await text_to_speech.convert(
            text=request.text,
            voice=request.voice,
            speed=request.speed,
            language=request.language
        )
        
        print(f"DEBUG: TTS service returned: {result}")
        print(f"DEBUG: Result type: {type(result)}")
        
        # Handle new return format from TTS service
        if isinstance(result, dict):
            print(f"DEBUG: Handling dict result")
            audio_file_path = result["audio_file_path"]
            original_text = result.get("original_text", request.text)
            translated_text = result.get("translated_text")
        else:
            print(f"DEBUG: Handling string result (fallback)")
            # Fallback for old format
            audio_file_path = result
            original_text = request.text
            translated_text = None
            
        print(f"DEBUG: Final response - text: {original_text}, translated: {translated_text}, language: {request.language}")
            
        return TextToSpeechResponse(
            text=original_text,
            translated_text=translated_text,
            audio_file_path=audio_file_path,
            duration=text_to_speech.get_audio_duration(audio_file_path),
            language=request.language
        )
    except Exception as e:
        print(f"DEBUG: Error in TTS endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speech-to-text", response_model=SpeechToTextResponse)
async def convert_speech_to_text(
    audio_file: UploadFile = File(...),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Convert speech to text with timestamps"""
    try:
        # Debug logging
        print(f"Received audio file: {audio_file.filename}")
        print(f"Content type: {audio_file.content_type}")
        print(f"File size: {audio_file.size if hasattr(audio_file, 'size') else 'unknown'}")
        
        # Check file extension
        file_extension = audio_file.filename.lower().split('.')[-1] if '.' in audio_file.filename else 'no_extension'
        print(f"Detected extension: {file_extension}")
        
        supported_extensions = ('.mp3', '.wav', '.m4a', '.flac', '.webm', '.mp4', '.ogg', '.aac')
        if not audio_file.filename.lower().endswith(supported_extensions):
            raise HTTPException(status_code=400, detail=f"Unsupported audio format: {audio_file.filename}. Supported formats: MP3, WAV, M4A, FLAC, WebM, MP4, OGG, AAC")
        
        transcript = await speech_to_text.transcribe(
            audio_file=audio_file,
            language="en-US",  # ISO-639-1 format: en-US, not en-us
            include_timestamps=True
        )
        return SpeechToTextResponse(
            transcript=transcript["text"],
            timestamps=transcript["timestamps"],
            confidence=transcript["confidence"]
        )
    except Exception as e:
        print(f"Error in speech-to-text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-document", response_model=DocumentProcessingResponse)
async def process_document(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Process various document formats and convert to accessible formats"""
    try:
        # Save uploaded file to temporary location
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Create unique filename
        import uuid
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        temp_filename = f"{uuid.uuid4()}{file_extension}"
        temp_file_path = os.path.join(temp_dir, temp_filename)
        
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        try:
            # Process the document
            result = await document_processor.process(
                file_path=temp_file_path,
                output_format="both",
                include_audio=True,
                include_simplified_text=True
            )
            
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
            return DocumentProcessingResponse(
                original_format=result["original_format"],
                output_formats=result["output_formats"],
                simplified_text=result.get("simplified_text"),
                audio_file_path=result.get("audio_file_path"),
                processing_time=result.get("processing_time"),
                file_size=result.get("file_size")
            )
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise e
            
    except Exception as e:
        print(f"Error in document processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{file_path:path}")
async def download_file(
    file_path: str
):
    """Download generated files"""
    try:
        full_path = os.path.join("temp", file_path)
        if os.path.exists(full_path):
            return FileResponse(full_path, filename=os.path.basename(file_path))
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 