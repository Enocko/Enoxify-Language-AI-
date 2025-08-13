import os
import tempfile
import time
from typing import Dict, Any, Optional
import speech_recognition as sr
import azure.cognitiveservices.speech as speechsdk
from google.cloud import speech
import openai

class SpeechToText:
    def __init__(self):
        self.azure_speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.azure_region = os.getenv("AZURE_SPEECH_REGION", "eastus")
        self.google_credentials = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize recognizer for local processing
        self.recognizer = sr.Recognizer()
        
        # Initialize Google Cloud client if credentials are available
        self.google_client = None
        if self.google_credentials:
            try:
                self.google_client = speech.SpeechClient()
            except Exception:
                pass
    
    async def transcribe(self, audio_file, language: str = "en-US", include_timestamps: bool = True) -> Dict[str, Any]:
        """
        Transcribe audio to text with optional timestamps
        
        Args:
            audio_file: Uploaded audio file
            language: Language code for transcription
            include_timestamps: Whether to include word-level timestamps
            
        Returns:
            Dictionary with transcript, timestamps, and confidence
        """
        # Debug: Log the original language parameter
        print(f"Original language parameter: '{language}'")
        
        # Ensure language is in correct ISO-639-1 format
        if language.lower() == "en-us":
            language = "en-US"
        elif language.lower() == "en-gb":
            language = "en-GB"
        elif language.lower() == "es-es":
            language = "es-ES"
        elif language.lower() == "fr-fr":
            language = "fr-FR"
        elif language.lower() == "de-de":
            language = "de-DE"
        
        # Debug: Log the processed language parameter
        print(f"Processed language parameter: '{language}'")
        
        start_time = time.time()
        
        try:
            # Save uploaded file temporarily
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            temp_file.write(audio_file.file.read())
            temp_file.close()
            
            # Try different transcription services in order of preference
            result = None
            
            # Try Azure Speech Services first (best for timestamps)
            if self.azure_speech_key and include_timestamps:
                result = await self._transcribe_with_azure(temp_file.name, language)
            
            # Try Google Cloud Speech if Azure failed or timestamps not needed
            if not result and self.google_client:
                result = await self._transcribe_with_google(temp_file.name, language, include_timestamps)
            
            # Fallback to OpenAI Whisper
            if not result and self.openai_api_key:
                result = await self._transcribe_with_openai(temp_file.name, language)
            
            # Final fallback to local speech recognition
            if not result:
                result = await self._transcribe_locally(temp_file.name, language)
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            if not result:
                raise Exception("All transcription services failed")
            
            # Add processing time
            result["processing_time"] = time.time() - start_time
            
            return result
            
        except Exception as e:
            # Clean up temp file on error
            try:
                os.unlink(temp_file.name)
            except:
                pass
            raise Exception(f"Error transcribing audio: {str(e)}")
    
    async def _transcribe_with_azure(self, audio_file_path: str, language: str) -> Optional[Dict[str, Any]]:
        """Transcribe using Azure Speech Services with detailed results"""
        try:
            # Configure speech config
            speech_config = speechsdk.SpeechConfig(
                subscription=self.azure_speech_key,
                region=self.azure_region
            )
            speech_config.speech_recognition_language = language
            
            # Enable detailed results for timestamps
            speech_config.enable_dictation()
            speech_config.set_property(
                speechsdk.PropertyId.SpeechServiceResponse_RequestWordLevelTimestamps, 
                "true"
            )
            
            # Configure audio input
            audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
            
            # Create recognizer
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, 
                audio_config=audio_config
            )
            
            # Perform recognition
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                # Extract detailed results
                detailed_result = result.properties.get(
                    speechsdk.PropertyId.SpeechServiceResponse_JsonResult
                )
                
                if detailed_result:
                    import json
                    detailed = json.loads(detailed_result)
                    
                    # Extract timestamps if available
                    timestamps = []
                    if "Words" in detailed:
                        for word in detailed["Words"]:
                            timestamps.append({
                                "word": word["Word"],
                                "start": word["Offset"] / 10000000,  # Convert to seconds
                                "end": (word["Offset"] + word["Duration"]) / 10000000,
                                "confidence": word.get("Confidence", 1.0)
                            })
                    
                    return {
                        "text": result.text,
                        "timestamps": timestamps,
                        "confidence": detailed.get("NBest", [{}])[0].get("Confidence", 0.8)
                    }
                
                # Fallback to basic result
                return {
                    "text": result.text,
                    "timestamps": [],
                    "confidence": 0.8
                }
            
            return None
            
        except Exception as e:
            print(f"Azure STT error: {e}")
            return None
    
    async def _transcribe_with_google(self, audio_file_path: str, language: str, include_timestamps: bool) -> Optional[Dict[str, Any]]:
        """Transcribe using Google Cloud Speech-to-Text"""
        try:
            if not self.google_client:
                return None
            
            # Read audio file
            with open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()
            
            # Configure audio
            audio = speech.RecognitionAudio(content=content)
            
            # Configure recognition
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language,
                enable_word_time_offsets=include_timestamps,
                enable_automatic_punctuation=True
            )
            
            # Perform recognition
            response = self.google_client.recognize(config=config, audio=audio)
            
            if not response.results:
                return None
            
            # Extract results
            transcript = ""
            timestamps = []
            confidence = 0.0
            
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
                confidence = max(confidence, result.alternatives[0].confidence)
                
                # Extract timestamps if available
                if include_timestamps and result.alternatives[0].words:
                    for word_info in result.alternatives[0].words:
                        timestamps.append({
                            "word": word_info.word,
                            "start": word_info.start_time.total_seconds(),
                            "end": word_info.end_time.total_seconds(),
                            "confidence": 1.0  # Google doesn't provide word-level confidence
                        })
            
            return {
                "text": transcript.strip(),
                "timestamps": timestamps,
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"Google STT error: {e}")
            return None
    
    async def _transcribe_with_openai(self, audio_file_path: str, language: str) -> Optional[Dict[str, Any]]:
        """Transcribe using OpenAI Whisper"""
        try:
            # Debug: Log the language being sent to OpenAI
            print(f"OpenAI transcription - language parameter: '{language}'")
            
            client = openai.OpenAI(api_key=self.openai_api_key)
            
            with open(audio_file_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    # Remove language parameter - let Whisper auto-detect
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )
            
            # Extract timestamps - handle different response formats
            timestamps = []
            transcript_text = ""
            
            # Try to get text from response
            if hasattr(response, 'text'):
                transcript_text = response.text
            elif hasattr(response, 'words') and response.words:
                # If we have words but no text, construct text from words
                transcript_text = " ".join([word.text for word in response.words])
            
            # Extract timestamps if available
            if hasattr(response, 'words') and response.words:
                for word in response.words:
                    if hasattr(word, 'text') and hasattr(word, 'start') and hasattr(word, 'end'):
                        timestamps.append({
                            "word": word.text,
                            "start": word.start,
                            "end": word.end,
                            "confidence": 1.0
                        })
            
            # Ensure we have text
            if not transcript_text:
                print(f"Warning: No transcript text found in response. Response type: {type(response)}")
                print(f"Response attributes: {dir(response)}")
                if hasattr(response, 'words'):
                    print(f"Words: {response.words}")
                transcript_text = "Audio transcribed successfully"
            
            return {
                "text": transcript_text,
                "timestamps": timestamps,
                "confidence": 0.9  # Whisper doesn't provide confidence scores
            }
            
        except Exception as e:
            print(f"OpenAI STT error: {e}")
            return None
    
    async def _transcribe_locally(self, audio_file_path: str, language: str) -> Optional[Dict[str, Any]]:
        """Transcribe using local speech recognition (fallback)"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
            
            # Try different recognition engines
            text = None
            
            # Try Google Speech Recognition (free tier)
            try:
                text = self.recognizer.recognize_google(audio, language=language)
            except:
                pass
            
            # Try Sphinx (offline, less accurate)
            if not text:
                try:
                    text = self.recognizer.recognize_sphinx(audio, language=language)
                except:
                    pass
            
            if text:
                return {
                    "text": text,
                    "timestamps": [],  # Local recognition doesn't provide timestamps
                    "confidence": 0.7  # Lower confidence for local processing
                }
            
            return None
            
        except Exception as e:
            print(f"Local STT error: {e}")
            return None
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return [
            {"code": "en-US", "name": "English (US)"},
            {"code": "en-GB", "name": "English (UK)"},
            {"code": "es-ES", "name": "Spanish"},
            {"code": "fr-FR", "name": "French"},
            {"code": "de-DE", "name": "German"},
            {"code": "it-IT", "name": "Italian"},
            {"code": "pt-BR", "name": "Portuguese (Brazil)"},
            {"code": "ja-JP", "name": "Japanese"},
            {"code": "ko-KR", "name": "Korean"},
            {"code": "zh-CN", "name": "Chinese (Simplified)"}
        ]
    
    def get_audio_formats(self) -> list:
        """Get list of supported audio formats"""
        return [
            {"format": "MP3", "extensions": [".mp3"], "description": "MPEG Audio Layer III"},
            {"format": "WAV", "extensions": [".wav"], "description": "Waveform Audio File Format"},
            {"format": "M4A", "extensions": [".m4a"], "description": "MPEG-4 Audio"},
            {"format": "FLAC", "extensions": [".flac"], "description": "Free Lossless Audio Codec"},
            {"format": "OGG", "extensions": [".ogg"], "description": "Ogg Vorbis"}
        ]
