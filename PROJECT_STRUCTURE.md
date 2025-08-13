# Project Structure Documentation

## Overview

The AI-Based Accessibility Enhancer is organized as a full-stack application with a clear separation of concerns between backend services and frontend components.

## Directory Structure

```
ai-accessibility-enhancer/
├── 📁 backend/                    # FastAPI Python backend
│   ├── 📁 app/                    # Application package
│   │   ├── 📁 models/            # Pydantic data models
│   │   │   ├── request_models.py  # API request schemas
│   │   │   └── response_models.py # API response schemas
│   │   ├── 📁 services/          # Core AI services
│   │   │   ├── text_simplifier.py # Text simplification using OpenAI
│   │   │   ├── text_to_speech.py # TTS using Azure/Google/OpenAI
│   │   │   ├── speech_to_text.py # STT using Google Cloud
│   │   │   └── document_processor.py # Document processing
│   │   └── 📁 utils/             # Utility functions
│   ├── 📄 main.py                # FastAPI application entry point
│   ├── 📄 requirements.txt       # Python dependencies
│   ├── 📄 .env.example          # Environment variables template
│   ├── 📄 Dockerfile            # Backend container configuration
│   └── 📄 test_main.py          # Comprehensive test suite
├── 📁 frontend/                  # React TypeScript frontend
│   ├── 📁 public/               # Static assets
│   ├── 📁 src/                  # Source code
│   │   ├── 📁 components/       # React components
│   │   │   ├── Header.tsx       # Application header
│   │   │   ├── TextSimplifier.tsx # Text simplification interface
│   │   │   ├── TextToSpeech.tsx # TTS interface
│   │   │   ├── SpeechToText.tsx # STT interface
│   │   │   └── DocumentProcessor.tsx # Document processing interface
│   │   ├── 📁 services/         # API client services
│   │   ├── 📁 types/            # TypeScript type definitions
│   │   ├── App.tsx              # Main application component
│   │   └── index.tsx            # Application entry point
│   ├── 📄 package.json          # Node.js dependencies
│   ├── 📄 tailwind.config.js    # Tailwind CSS configuration
│   └── 📄 Dockerfile            # Frontend container configuration
├── 📄 demo.py                    # Standalone demo script
├── 📄 docker-compose.yml        # Multi-container deployment
├── 📄 setup.sh                  # Automated setup script
├── 📄 README.md                 # Project documentation
└── 📄 PROJECT_STRUCTURE.md      # This file
```

## Backend Architecture

### Core Services

#### 1. Text Simplifier (`text_simplifier.py`)
- **Purpose**: Converts complex academic text to simpler language
- **AI Provider**: OpenAI GPT-4
- **Features**:
  - Multiple reading levels (elementary, middle school, high school, college)
  - Meaning preservation
  - Readability scoring (Flesch Reading Ease)
  - Statistics and metrics

#### 2. Text-to-Speech (`text_to_speech.py`)
- **Purpose**: Converts text to natural-sounding audio
- **AI Providers**: Azure Speech Services (primary), Google Cloud TTS, OpenAI TTS (fallback)
- **Features**:
  - Voice customization (male, female, neutral)
  - Speed control
  - Multiple language support
  - Automatic service fallback

#### 3. Speech-to-Text (`speech_to_text.py`)
- **Purpose**: Converts audio to text with timestamps
- **AI Provider**: Google Cloud Speech-to-Text
- **Features**:
  - Word-level timestamps
  - Confidence scoring
  - Language detection
  - Multiple audio format support

#### 4. Document Processor (`document_processor.py`)
- **Purpose**: Processes various document formats
- **Supported Formats**: PDF, DOCX, TXT, images
- **Features**:
  - Multi-format input handling
  - Batch processing
  - Output format selection
  - Progress tracking

### Data Models

#### Request Models (`request_models.py`)
- `TextSimplificationRequest`: Text simplification parameters
- `TextToSpeechRequest`: TTS conversion parameters
- `DocumentProcessingRequest`: Document processing parameters

#### Response Models (`response_models.py`)
- `TextSimplificationResponse`: Simplified text and metrics
- `TextToSpeechResponse`: Audio file information
- `SpeechToTextResponse`: Transcription with timestamps
- `DocumentProcessingResponse`: Processing results

## Frontend Architecture

### Component Structure

#### 1. Header (`Header.tsx`)
- Application title and navigation
- Accessibility information
- User preferences

#### 2. Text Simplifier (`TextSimplifier.tsx`)
- Text input area
- Reading level selection
- Meaning preservation toggle
- Results display with readability metrics

#### 3. Text-to-Speech (`TextToSpeech.tsx`)
- Text input
- Voice and speed controls
- Audio playback controls
- Download functionality

#### 4. Speech-to-Text (`SpeechToText.tsx`)
- Audio file upload
- Recording interface
- Transcription display
- Timestamp visualization

#### 5. Document Processor (`DocumentProcessor.tsx`)
- File upload interface
- Format selection
- Processing options
- Results display

### State Management
- React hooks for local state
- API service layer for backend communication
- Toast notifications for user feedback
- Error handling and loading states

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/` | GET | API information | - | Basic info |
| `/health` | GET | Service health | - | Health status |
| `/simplify-text` | POST | Simplify text | Text + options | Simplified text + metrics |
| `/text-to-speech` | POST | Convert to audio | Text + voice options | Audio file path + duration |
| `/speech-to-text` | POST | Convert to text | Audio file | Transcript + timestamps |
| `/process-document` | POST | Process documents | File + options | Processing results |
| `/download/{file}` | GET | Download files | - | File download |

### Request/Response Flow

```
Frontend → API Gateway → Service Layer → AI Provider → Response → Frontend
    ↓           ↓           ↓           ↓           ↓         ↓
  User Input → Validation → Processing → AI Call → Format → Display
```

## Configuration

### Environment Variables

#### Required
- `OPENAI_API_KEY`: OpenAI API key for text simplification

#### Optional
- `AZURE_SPEECH_KEY`: Azure Speech Services key
- `AZURE_SPEECH_REGION`: Azure region
- `GOOGLE_CLOUD_CREDENTIALS`: Google Cloud service account path

### Service Configuration

#### Text Simplifier
- Model: GPT-4
- Temperature: 0.3 (for consistent output)
- Max tokens: 2000
- Reading level presets

#### Text-to-Speech
- Primary: Azure Speech Services
- Fallback: Google Cloud TTS
- Final fallback: OpenAI TTS
- Voice mapping and customization

#### Speech-to-Text
- Provider: Google Cloud Speech-to-Text
- Language detection
- Timestamp generation
- Confidence scoring

## Testing Strategy

### Backend Testing
- Unit tests for each service
- Integration tests for API endpoints
- Mock AI providers for testing
- Performance and load testing

### Frontend Testing
- Component unit tests
- Integration tests for user flows
- Accessibility testing
- Cross-browser compatibility

### Test Coverage
- Core functionality: 90%+
- Error handling: 100%
- Edge cases: 80%+
- Performance: Load testing

## Deployment

### Development
- Local development servers
- Hot reloading
- Environment variable management
- Debug logging

### Production
- Docker containerization
- Load balancing
- Monitoring and logging
- Auto-scaling
- CDN for static assets

### CI/CD Pipeline
- Automated testing
- Code quality checks
- Security scanning
- Automated deployment

## Security Considerations

### API Security
- Input validation
- File type restrictions
- Size limits
- Rate limiting

### Data Privacy
- Temporary file storage
- Automatic cleanup
- No persistent storage of user content
- Secure API key management

### Access Control
- CORS configuration
- Request validation
- Error message sanitization

## Performance Optimization

### Backend
- Async processing
- Connection pooling
- Caching strategies
- Resource management

### Frontend
- Lazy loading
- Component optimization
- Bundle splitting
- Image optimization

### Infrastructure
- Load balancing
- Auto-scaling
- CDN distribution
- Database optimization

## Monitoring and Logging

### Application Metrics
- Request/response times
- Error rates
- Success rates
- Resource usage

### Business Metrics
- Text simplification usage
- Audio conversion volume
- Document processing counts
- User engagement

### Logging
- Structured logging
- Error tracking
- Performance monitoring
- Audit trails

## Future Enhancements

### Planned Features
- User authentication
- Batch processing
- Advanced analytics
- Mobile applications
- API rate limiting
- Webhook support

### Scalability Improvements
- Microservices architecture
- Message queuing
- Distributed processing
- Multi-region deployment

### AI Enhancements
- Custom model training
- Multi-language support
- Advanced accessibility features
- Real-time processing 