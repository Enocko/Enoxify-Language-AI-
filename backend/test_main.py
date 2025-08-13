import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
import tempfile
import os

# Import the FastAPI app
from main import app

# Create test client
client = TestClient(app)

class TestTextSimplifier:
    """Test text simplification functionality"""
    
    @pytest.mark.asyncio
    async def test_simplify_text_success(self):
        """Test successful text simplification"""
        with patch('app.services.text_simplifier.TextSimplifier.simplify') as mock_simplify:
            mock_simplify.return_value = "This is simplified text."
            
            response = client.post("/simplify-text", json={
                "text": "Complex academic text here.",
                "target_level": "middle_school",
                "preserve_meaning": True
            })
            
            assert response.status_code == 200
            data = response.json()
            assert "simplified_text" in data
            assert data["simplified_text"] == "This is simplified text."
    
    @pytest.mark.asyncio
    async def test_simplify_text_invalid_level(self):
        """Test text simplification with invalid reading level"""
        response = client.post("/simplify-text", json={
            "text": "Test text",
            "target_level": "invalid_level",
            "preserve_meaning": True
        })
        
        assert response.status_code == 200  # Should still work with fallback
    
    def test_readability_calculation(self):
        """Test readability score calculation"""
        from app.services.text_simplifier import TextSimplifier
        
        simplifier = TextSimplifier()
        score = simplifier.calculate_readability("Simple text. Easy to read.")
        
        assert isinstance(score, float)
        assert 0 <= score <= 100

class TestTextToSpeech:
    """Test text-to-speech functionality"""
    
    @pytest.mark.asyncio
    async def test_text_to_speech_success(self):
        """Test successful text-to-speech conversion"""
        with patch('app.services.text_to_speech.TextToSpeech.convert') as mock_convert:
            mock_convert.return_value = "/tmp/test_audio.mp3"
            
            response = client.post("/text-to-speech", json={
                "text": "Hello world",
                "voice": "neutral",
                "speed": 1.0,
                "language": "en-US"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert "audio_file_path" in data
            assert data["audio_file_path"] == "/tmp/test_audio.mp3"
    
    @pytest.mark.asyncio
    async def test_text_to_speech_voice_options(self):
        """Test different voice options"""
        voices = ["male", "female", "neutral"]
        
        for voice in voices:
            with patch('app.services.text_to_speech.TextToSpeech.convert') as mock_convert:
                mock_convert.return_value = f"/tmp/test_{voice}.mp3"
                
                response = client.post("/text-to-speech", json={
                    "text": "Test text",
                    "voice": voice,
                    "speed": 1.0,
                    "language": "en-US"
                })
                
                assert response.status_code == 200

class TestSpeechToText:
    """Test speech-to-text functionality"""
    
    def test_speech_to_text_file_validation(self):
        """Test audio file format validation"""
        # Test with invalid file type
        with tempfile.NamedTemporaryFile(suffix=".txt") as temp_file:
            temp_file.write(b"Not an audio file")
            temp_file.flush()
            
            with open(temp_file.name, 'rb') as f:
                response = client.post("/speech-to-text", files={"audio_file": f})
                
                assert response.status_code == 400
                assert "Unsupported audio format" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_speech_to_text_success(self):
        """Test successful speech-to-text conversion"""
        with patch('app.services.speech_to_text.SpeechToText.transcribe') as mock_transcribe:
            mock_transcribe.return_value = {
                "text": "This is transcribed text",
                "timestamps": [{"word": "This", "start": 0.0, "end": 0.5, "confidence": 0.95}],
                "confidence": 0.95
            }
            
            # Create a mock audio file
            with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
                temp_file.write(b"fake audio data")
                temp_file.flush()
                
                with open(temp_file.name, 'rb') as f:
                    response = client.post("/speech-to-text", files={"audio_file": f})
                    
                    assert response.status_code == 200
                    data = response.json()
                    assert "transcript" in data
                    assert "timestamps" in data
                    assert "confidence" in data

class TestDocumentProcessor:
    """Test document processing functionality"""
    
    @pytest.mark.asyncio
    async def test_document_processing_success(self):
        """Test successful document processing"""
        with patch('app.services.document_processor.DocumentProcessor.process') as mock_process:
            mock_process.return_value = {
                "original_format": "PDF",
                "output_formats": ["simplified_text", "audio"],
                "simplified_text": "Simplified document content",
                "audio_file_path": "/tmp/test_audio.mp3"
            }
            
            response = client.post("/process-document", json={
                "file_path": "test.pdf",
                "output_format": "both",
                "include_audio": True,
                "include_simplified_text": True
            })
            
            assert response.status_code == 200
            data = response.json()
            assert "original_format" in data
            assert "output_formats" in data
            assert "simplified_text" in data
            assert "audio_file_path" in data

class TestAPIEndpoints:
    """Test general API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert "status" in response.json()
        assert "services" in response.json()
    
    def test_download_file_not_found(self):
        """Test download endpoint with non-existent file"""
        response = client.get("/download/nonexistent_file.mp3")
        assert response.status_code == 404
        assert "File not found" in response.json()["detail"]

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_malformed_json(self):
        """Test handling of malformed JSON"""
        response = client.post("/simplify-text", data="invalid json")
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        response = client.post("/simplify-text", json={})
        assert response.status_code == 422
    
    def test_large_text_input(self):
        """Test handling of very large text input"""
        large_text = "A" * 10000  # 10KB of text
        
        with patch('app.services.text_simplifier.TextSimplifier.simplify') as mock_simplify:
            mock_simplify.return_value = "Simplified large text"
            
            response = client.post("/simplify-text", json={
                "text": large_text,
                "target_level": "middle_school",
                "preserve_meaning": True
            })
            
            assert response.status_code == 200

class TestPerformance:
    """Test performance characteristics"""
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return client.post("/health")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(5)]
            responses = [future.result() for future in futures]
            
            for response in responses:
                assert response.status_code == 200

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 