from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TextSimplificationResponse(BaseModel):
    original_text: str
    simplified_text: str
    readability_score: float
    processing_time: Optional[float] = None

class TextToSpeechResponse(BaseModel):
    text: str
    translated_text: Optional[str] = None
    audio_file_path: str
    duration: float
    language: str
    processing_time: Optional[float] = None

class SpeechToTextResponse(BaseModel):
    transcript: str
    timestamps: List[Dict[str, Any]]
    confidence: float
    processing_time: Optional[float] = None

class DocumentProcessingResponse(BaseModel):
    original_format: str
    output_formats: List[str]
    simplified_text: Optional[str] = None
    audio_file_path: Optional[str] = None
    processing_time: Optional[float] = None
    file_size: Optional[int] = None

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str
