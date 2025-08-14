import os
import tempfile
import time
import uuid
from typing import Optional
from gtts import gTTS
import openai

class TextToSpeech:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
    async def convert(self, text: str, voice: str = "neutral", speed: float = 1.0, language: str = "en-US") -> dict:
        """
        Convert text to speech using gTTS with proper language support
        
        Args:
            text: Text to convert
            voice: Voice type (male, female, neutral) - not used by gTTS
            speed: Speech speed multiplier - not used by gTTS (handled by frontend)
            language: Language code (e.g., 'en-US', 'es', 'fr', 'de')
            
        Returns:
            Dictionary containing:
            - audio_file_path: Path to the generated audio file
            - original_text: The original input text
            - translated_text: The translated text (if translation occurred)
            - language: The target language
        """
        start_time = time.time()
        
        try:
            # Map language codes to gTTS language codes
            lang_code = self._map_language_code(language)
            print(f"DEBUG: Original language: {language}, Mapped to: {lang_code}")
            
            original_text = text  # Store original text
            
            # For non-English languages, we need to translate the text first
            if lang_code not in ['en', 'en-GB']:
                print(f"DEBUG: Non-English language detected: {lang_code}, attempting translation...")
                translated_text = await self._translate_text(text, lang_code)
                if translated_text:
                    print(f"DEBUG: Translation successful. Original: '{text[:50]}...', Translated: '{translated_text[:50]}...'")
                    text = translated_text
                else:
                    print(f"DEBUG: Translation failed for {lang_code}")
            else:
                print(f"DEBUG: English language detected: {lang_code}, no translation needed")
            
            print(f"DEBUG: Final text to convert: '{text[:50]}...'")
            
            # Create gTTS instance with proper language configuration
            if lang_code == 'en-GB':
                # British English
                tts = gTTS(text=text, lang="en", tld="co.uk", slow=False)
            elif lang_code == 'en':
                # US English
                tts = gTTS(text=text, lang="en", slow=False)
            else:
                # Other languages
                tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Create temp directory if it doesn't exist
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Create unique filename in temp directory
            temp_filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
            temp_file_path = os.path.join(temp_dir, temp_filename)
            
            # Generate speech
            tts.save(temp_file_path)
            
            print(f"gTTS generated audio for {language} in {time.time() - start_time:.2f}s")
            
            # Return both original and translated text for frontend display
            return {
                "audio_file_path": temp_filename,  # Return just the filename, not full path
                "original_text": original_text,
                "translated_text": text if text != original_text else None,
                "language": language
            }
            
        except Exception as e:
            raise Exception(f"Error converting text to speech: {str(e)}")
    
    def _map_language_code(self, language: str) -> str:
        """Map language codes to gTTS compatible codes"""
        language_mapping = {
            'en-US': 'en',
            'en-GB': 'en-GB',
            'es': 'es',
            'fr': 'fr',
            'de': 'de'
        }
        return language_mapping.get(language, 'en')
    
    async def _translate_text(self, text: str, target_language: str) -> Optional[str]:
        """Translate text to target language using OpenAI"""
        try:
            if not self.openai_api_key:
                print("OpenAI API key not available, skipping translation")
                return None
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            # Map language codes to language names for better translation
            language_names = {
                'es': 'Spanish',
                'fr': 'French',
                'de': 'German'
            }
            
            target_lang_name = language_names.get(target_language, target_language)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a professional translator. Translate the following text to {target_lang_name}. Maintain the original meaning and tone. Only return the translated text, nothing else."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=0.1
            )
            
            translated_text = response.choices[0].message.content.strip()
            print(f"Translated text to {target_language}: {translated_text[:50]}...")
            return translated_text
            
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    def get_audio_duration(self, file_path: str) -> float:
        """Get audio duration (placeholder - gTTS doesn't provide duration)"""
        # gTTS doesn't provide duration, so we estimate based on text length
        # Average speaking rate is about 150 words per minute
        return 5.0  # Placeholder duration
    
    def get_available_voices(self, language: str = "en-US") -> list:
        """Get list of available voices for a language"""
        voices = []
        
        # gTTS doesn't have a direct concept of "voices" like Azure or Google Cloud
        # This method will return an empty list as gTTS is a single-voice engine.
        return voices
    
    def cleanup_temp_files(self, file_paths: list):
        """Clean up temporary audio files"""
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception:
                pass
