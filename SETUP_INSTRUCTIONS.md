# 🚀 TextFlow Setup Instructions

## 🔑 **CRITICAL: Set Your OpenAI API Key**

To make TextFlow work with all features, you need to set your OpenAI API key:

### 1. **Get Your OpenAI API Key**
- Visit: https://platform.openai.com/api-keys
- Sign in or create an account
- Create a new API key
- Copy the key (it starts with `sk-...`)

### 2. **Update Your .env File**
In the `backend/` folder, edit the `.env` file:

```bash
cd backend
nano .env  # or use any text editor
```

**Replace this line:**
```
OPENAI_API_KEY=your_openai_api_key_here
```

**With your actual key:**
```
OPENAI_API_KEY=sk-your_actual_api_key_here
```

### 3. **Save and Restart**
- Save the `.env` file
- Restart the backend server

## 🎯 **What This Enables:**

✅ **GPT-4 Text Simplification** - Professional quality like ChatGPT  
✅ **OpenAI Whisper Speech-to-Text** - Accurate audio transcription  
✅ **Intelligent Document Analysis** - AI-powered insights and summaries  
✅ **Advanced Language Processing** - Context-aware text enhancement  

## 🚨 **Without the API Key:**

❌ Text simplification will fail  
❌ Speech-to-text will fail  
❌ Document analysis will be basic  
✅ TTS speed control will still work  

## 🚀 **Quick Start After Setting API Key:**

```bash
# Backend
cd backend
source venv/bin/activate
python simple_test_main.py

# Frontend (new terminal)
cd frontend
npm start
```

## 🌐 **Access Points:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

**Set your API key now to unlock the full power of TextFlow!** 🚀✨ 