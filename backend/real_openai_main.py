from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv
import asyncio
import time
import re
from openai import OpenAI
from pydantic import BaseModel

class TextSimplificationRequest(BaseModel):
    text: str
    target_level: str = "medium"
    preserve_meaning: bool = True

class TextSimplificationResponse(BaseModel):
    simplified_text: str
    readability_score: float
    success: bool
    error_message: str = None

class RealOpenAITextSimplifier:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY in .env file")
        
        self.client = OpenAI(api_key=api_key)
        
    async def simplify(self, text: str, target_level: str, preserve_meaning: bool) -> str:
        try:
            # Create a clear, specific prompt based on reading level
            if target_level == "basic":
                level_description = "elementary school student (ages 6-10)"
                instruction = "Use very simple words and very short sentences. Break complex ideas into simple parts."
            elif target_level == "medium":
                level_description = "middle school student (ages 11-14)"
                instruction = "Use simpler words and shorter sentences. Explain complex terms in simple ways."
            else:  # advanced
                level_description = "high school student (ages 15-18)"
                instruction = "Use clear, accessible language while maintaining academic tone. Simplify complex concepts."
            
            prompt = f"""Rewrite the following text so that it is understandable to a {level_description}, keeping all important information but using simpler vocabulary and shorter sentences.

{instruction}

Original text: "{text}"

Simplified version:"""

            print(f"🔍 Calling OpenAI API with prompt for {target_level} level...")
            print(f"📝 Original text length: {len(text)} characters")
            
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-4o-mini",  # Using GPT-4o-mini for cost efficiency
                messages=[
                    {"role": "system", "content": "You are an expert educator who specializes in making complex text accessible to students at different reading levels. Always provide clear, accurate, and educationally appropriate simplifications."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3  # Lower temperature for more consistent results
            )
            
            simplified_text = response.choices[0].message.content.strip()
            
            # Remove quotes if the AI wrapped the response in them
            if simplified_text.startswith('"') and simplified_text.endswith('"'):
                simplified_text = simplified_text[1:-1]
            
            print(f"✅ OpenAI API call successful")
            print(f"📝 Simplified text length: {len(simplified_text)} characters")
            
            return simplified_text
            
        except Exception as e:
            error_msg = f"OpenAI API error: {str(e)}"
            print(f"❌ {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)

    def calculate_readability(self, text: str) -> float:
        """Calculate Flesch Reading Ease score"""
        try:
            words = text.split()
            sentences = [s for s in text.split('.') if s.strip()]
            syllables = self._count_syllables(text)
            
            if len(words) == 0 or len(sentences) == 0:
                return 0.0
            
            avg_sentence_length = len(words) / len(sentences)
            avg_syllables_per_word = syllables / len(words)
            
            score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            return max(0.0, min(100.0, score))
        except:
            return 0.0
    
    def _count_syllables(self, text: str) -> int:
        text = text.lower()
        count = 0
        vowels = 'aeiouy'
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        return max(1, count)

# Initialize FastAPI app
load_dotenv()
app = FastAPI(
    title="AI-Based Accessibility Enhancer (Real OpenAI Mode)", 
    description="Convert educational content into accessible formats using OpenAI GPT-4o-mini for real text simplification", 
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000", "http://localhost:8000"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Initialize the text simplifier
try:
    text_simplifier = RealOpenAITextSimplifier()
    print("🚀 OpenAI text simplifier initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize OpenAI text simplifier: {e}")
    text_simplifier = None

@app.get("/")
async def root():
    return {
        "message": "AI-Based Accessibility Enhancer API (Real OpenAI Mode)",
        "status": "running",
        "text_simplifier": "available" if text_simplifier else "unavailable"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if text_simplifier else "unhealthy",
        "services": ["text_simplifier"] if text_simplifier else [],
        "mode": "real_openai",
        "openai_configured": text_simplifier is not None
    }

@app.post("/simplify-text", response_model=TextSimplificationResponse)
async def simplify_text(request: TextSimplificationRequest):
    if not text_simplifier:
        return TextSimplificationResponse(
            simplified_text="",
            readability_score=0.0,
            success=False,
            error_message="OpenAI text simplifier not available. Please check API configuration."
        )
    
    try:
        print(f"📥 Received simplification request for {request.target_level} level")
        print(f"📝 Text: {request.text[:100]}{'...' if len(request.text) > 100 else ''}")
        
        simplified_text = await text_simplifier.simplify(
            request.text, 
            request.target_level, 
            request.preserve_meaning
        )
        
        readability_score = text_simplifier.calculate_readability(simplified_text)
        
        print(f"✅ Simplification successful. Readability score: {readability_score:.1f}")
        
        return TextSimplificationResponse(
            simplified_text=simplified_text,
            readability_score=readability_score,
            success=True
        )
        
    except Exception as e:
        error_msg = f"Text simplification failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        return TextSimplificationResponse(
            simplified_text="",
            readability_score=0.0,
            success=False,
            error_message=error_msg
        )

if __name__ == "__main__":
    print("🚀 Starting AI-Based Accessibility Enhancer (Real OpenAI Mode)")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("🔧 This version uses REAL OpenAI GPT-4o-mini API calls")
    
    if not text_simplifier:
        print("⚠️  WARNING: OpenAI API not configured. Text simplification will not work.")
        print("   Please set your OPENAI_API_KEY in the .env file")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
