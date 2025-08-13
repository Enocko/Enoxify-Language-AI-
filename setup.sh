#!/bin/bash

# AI-Based Accessibility Enhancer Setup Script
# This script will set up the entire project environment

set -e

echo "🚀 Setting up AI-Based Accessibility Enhancer..."
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment for backend
echo "🐍 Setting up Python backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your API keys before running the application"
else
    echo "✅ .env file already exists"
fi

# Create temp directory
mkdir -p temp

cd ..

# Setup frontend
echo "⚛️  Setting up React frontend..."
cd frontend

echo "Installing Node.js dependencies..."
npm install

cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p temp

# Make setup script executable
chmod +x setup.sh

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit backend/.env with your API keys:"
echo "   - OPENAI_API_KEY (required for text simplification)"
echo "   - AZURE_SPEECH_KEY (optional, for high-quality TTS)"
echo "   - AZURE_SPEECH_REGION (optional)"
echo "   - GOOGLE_CLOUD_CREDENTIALS (optional)"
echo ""
echo "2. Start the backend:"
echo "   cd backend && source venv/bin/activate && python main.py"
echo ""
echo "3. Start the frontend (in a new terminal):"
echo "   cd frontend && npm start"
echo ""
echo "4. Or use Docker (if you have Docker installed):"
echo "   docker-compose up --build"
echo ""
echo "🌐 Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "🧪 Test without API keys:"
echo "   python demo.py"
echo ""
echo "Happy coding! 🚀" 