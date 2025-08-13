# 🎯 Enoxify - AI-Powered Accessibility Platform

A comprehensive AI-powered platform that makes complex information accessible to everyone through text simplification, multi-language text-to-speech, speech-to-text transcription, and intelligent document processing.

## ✨ Features

### 🔤 Text Simplification
- **AI-Powered Simplification**: Uses OpenAI GPT-4 to simplify complex text
- **Multiple Reading Levels**: Elementary, Middle School, High School, College
- **Meaning Preservation**: Maintains original content while improving readability
- **Grammar Enhancement**: Ensures perfect grammar and natural flow

### 🗣️ Multi-Language Text-to-Speech
- **Native Language Support**: Spanish, French, German, and more
- **AI Translation**: Automatically translates text to selected language
- **Dynamic Speed Control**: 0.5x to 2x playback speed
- **High-Quality Audio**: Powered by Google Text-to-Speech (gTTS)

### 🎤 Speech-to-Text
- **Live Recording**: Record audio directly in the browser
- **File Upload**: Support for MP4, WebM, OGG, AAC formats
- **AI Transcription**: Powered by OpenAI Whisper API
- **Real-Time Processing**: Instant text conversion

### 📄 Document Processing
- **Multi-Format Support**: PDF, Word documents
- **Intelligent Analysis**: AI-powered content summarization
- **Audio Output**: Convert documents to speech
- **Simplified Versions**: Generate accessible text versions

### 🎨 Beautiful 3D UI
- **Interactive Background**: 3D Rubik's Cube with glass-morphism effects
- **Modern Design**: Tab-based navigation with smooth transitions
- **Responsive Layout**: Works perfectly on all devices
- **Accessibility Focused**: Designed with accessibility in mind

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/enoxify.git
cd enoxify
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy the environment template
cp env_template.txt .env

# Edit .env with your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
```

### 4. Frontend Setup
```bash
cd ../frontend
npm install
```

### 5. Start the Application
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

Visit `http://localhost:3001` to use the application!

## 🔐 Security & Environment Variables

### Important Security Notes
- **Never commit your `.env` file** - it's already in `.gitignore`
- **Keep your OpenAI API key private** - it's linked to your account
- **Use environment variables** for all sensitive configuration

### Required Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Getting Your OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key to your `.env` file
4. Keep it secure and never share it

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI**: Modern, fast web framework
- **OpenAI Integration**: GPT-4 for text processing, Whisper for STT
- **gTTS**: Google Text-to-Speech for audio generation
- **Async Processing**: Non-blocking operations for better performance

### Frontend (React + TypeScript)
- **React 18**: Latest React with hooks and modern patterns
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Three.js**: 3D graphics and animations

### Key Technologies
- **AI Services**: OpenAI GPT-4, Whisper API
- **Audio Processing**: gTTS, MediaRecorder API
- **Document Handling**: PyPDF2, python-docx
- **3D Graphics**: Three.js, React Three Fiber

## 📁 Project Structure

```
enoxify/
├── backend/
│   ├── app/
│   │   ├── models/          # Pydantic models
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utility functions
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (not in git)
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── types/          # TypeScript types
│   ├── package.json         # Node.js dependencies
│   └── tailwind.config.js   # Tailwind configuration
├── .gitignore               # Git ignore rules
├── env_template.txt         # Environment template
└── README.md               # This file
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
source venv/bin/activate
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Backend Deployment
- **Docker**: Use the provided Dockerfile
- **Cloud Platforms**: Deploy to Heroku, Railway, or AWS
- **Environment Variables**: Set `OPENAI_API_KEY` in your deployment platform

### Frontend Deployment
- **Build**: `npm run build`
- **Static Hosting**: Deploy to Vercel, Netlify, or GitHub Pages
- **Environment**: Update API endpoints for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing powerful AI APIs
- **Google** for Text-to-Speech services
- **FastAPI** for the excellent web framework
- **React** for the amazing frontend library
- **Three.js** for 3D graphics capabilities

## 📞 Support

If you have any questions or need help:
- Create an issue on GitHub
- Check the documentation
- Review the code examples

---

**Made with ❤️ by the Enoxify Team**

*Empowering accessibility through AI innovation*
