# 🚀 Quick Start Guide

> **Get the AI-Based Accessibility Enhancer running in 5 minutes!**

## ⚡ Super Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Clone and setup everything automatically
git clone <repository-url>
cd ai-accessibility-enhancer
./setup.sh
```

### Option 2: Manual Setup
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# Frontend
cd ../frontend
npm install
```

## 🎯 What You'll Get

- **📝 Text Simplifier**: Complex → Simple language
- **🔊 Text-to-Speech**: Text → Natural audio
- **🎤 Speech-to-Text**: Audio → Text with timestamps  
- **📄 Document Processor**: PDF/DOCX → Accessible formats
- **📊 Readability Analysis**: Detailed accessibility metrics

## 🔑 Required API Keys

### Essential (Required)
- **OpenAI API Key**: For text simplification
  - Get at: https://platform.openai.com/api-keys
  - Add to: `backend/.env` as `OPENAI_API_KEY=your_key_here`

### Optional (Enhanced Features)
- **Azure Speech Services**: Better TTS quality
  - Get at: https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/
  - Add to: `backend/.env` as `AZURE_SPEECH_KEY=your_key_here`

- **Google Cloud**: Alternative TTS/STT
  - Get at: https://cloud.google.com/speech-to-text
  - Add to: `backend/.env` as `GOOGLE_CLOUD_CREDENTIALS=path/to/service-account.json`

## 🚀 Start the Application

### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

### Terminal 2: Frontend
```bash
cd frontend
npm start
```

### Access Your App
- 🌐 **Frontend**: http://localhost:3000
- 🔌 **Backend API**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

## 🧪 Test Without API Keys

```bash
python demo.py
```

This runs a full demo with mock AI services - perfect for testing the interface!

## 🐳 Docker Option

```bash
# Start everything with Docker
docker-compose up --build

# Access at http://localhost:3000
```

## 📱 First Steps

1. **Open** http://localhost:3000
2. **Try Text Simplifier**: Paste complex text, select reading level
3. **Test TTS**: Convert text to speech with different voices
4. **Upload Audio**: Test speech recognition
5. **Process Documents**: Upload PDFs for accessibility conversion

## 🔧 Troubleshooting

### Common Issues

**Backend won't start?**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend won't start?**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

**API errors?**
- Check your `.env` file has correct API keys
- Verify backend is running on port 8000
- Check browser console for CORS issues

**Port already in use?**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Get Help

- 📖 **Full Documentation**: README.md
- 🏗️ **Architecture**: PROJECT_STRUCTURE.md
- 🧪 **Tests**: `backend/test_main.py`
- 🐛 **Issues**: GitHub Issues

## 🎉 You're Ready!

Your AI-Based Accessibility Enhancer is now running! 

**Next steps:**
- Explore all the features
- Try different reading levels
- Test with your own content
- Customize voices and settings
- Share with others who need accessibility features

---

**Happy accessibility enhancing! 🚀** 