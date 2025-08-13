from pydantic import BaseModel, Field
from typing import Optional, Literal

class TextSimplificationRequest(BaseModel):
    text: str = Field(..., description="Text to be simplified", min_length=1, max_length=10000)
    target_level: Literal["elementary", "middle_school", "high_school", "college"] = Field(
        default="middle_school", 
        description="Target reading level for simplification"
    )
    preserve_meaning: bool = Field(
        default=True, 
        description="Whether to preserve the original meaning while simplifying"
    )

class TextToSpeechRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech", min_length=1, max_length=5000)
    voice: Literal["male", "female", "neutral"] = Field(
        default="neutral", 
        description="Voice type for speech synthesis"
    )
    speed: float = Field(
        default=1.0, 
        ge=0.5, le=2.0, 
        description="Speech speed multiplier"
    )
    language: str = Field(
        default="en-US", 
        description="Language code for speech synthesis"
    )

class DocumentProcessingRequest(BaseModel):
    file_path: str = Field(..., description="Path to the document file")
    output_format: Literal["audio", "simplified_text", "both"] = Field(
        default="both", 
        description="Desired output format"
    )
    include_audio: bool = Field(
        default=True, 
        description="Whether to include audio output"
    )
    include_simplified_text: bool = Field(
        default=True, 
        description="Whether to include simplified text output"
    )
