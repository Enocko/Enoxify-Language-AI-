#!/bin/bash

# Aivana - AI-Powered Text Enhancement Platform
# Startup script for backend and frontend services

echo "🚀 Starting Aivana - AI-Powered Text Enhancement Platform"
echo "========================================================"

# Function to cleanup processes
cleanup() {
    echo "🛑 Stopping services..."
    pkill -f "python.*main.py" 2>/dev/null
    pkill -f "python.*simple_test_main.py" 2>/dev/null
    pkill -f "uvicorn" 2>/dev/null
    pkill -f "npm start" 2>/dev/null
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Check if backend is already running and kill it
echo "🔍 Checking for existing backend processes..."
pkill -f "python.*main.py" 2>/dev/null
pkill -f "python.*simple_test_main.py" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null

# Wait a moment for processes to stop
sleep 2

# Start backend
echo "🐍 Starting Python backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔧 Activating virtual environment..."
source venv/bin/activate

echo "📥 Installing/updating dependencies..."
pip install -r requirements.txt

echo "🚀 Starting backend server..."
echo "   Note: Backend will support WebM, MP4, OGG, AAC audio formats"
python main.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "❌ Backend failed to start. Check the logs above."
    exit 1
fi

# Start frontend
echo "🌐 Starting React frontend..."
cd ../frontend

echo "📦 Installing/updating dependencies..."
npm install

echo "🚀 Starting frontend development server..."
npm start &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 10

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running on http://localhost:3000"
else
    echo "❌ Frontend failed to start. Check the logs above."
    exit 1
fi

echo ""
echo "🎉 Aivana is now running!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🎤 Audio Recording Features:"
echo "   ✅ Live recording with microphone"
echo "   ✅ Support for WebM, MP4, OGG, AAC formats"
echo "   ✅ File upload for existing audio files"
echo "   ✅ Speech-to-text conversion"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 