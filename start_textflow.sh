#!/bin/bash

# Aivana Startup Script
# This script starts both the backend and frontend services

echo "🚀 Starting Aivana - AI-Powered Text Enhancement"
echo "=================================================="

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY environment variable is not set!"
    echo "   Please set your OpenAI API key to use all features."
    echo "   You can get one from: https://platform.openai.com/api-keys"
    echo ""
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use. Stopping existing process..."
        lsof -ti:$1 | xargs kill -9
        sleep 2
    fi
}

# Check and clear ports
check_port 8000
check_port 3000

echo "🔧 Starting Backend Server..."
cd backend

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements_simple.txt

# Start backend in background
echo "🚀 Starting backend server on port 8000..."
python simple_test_main.py &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 8

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend server is running on http://localhost:8000"
else
    echo "❌ Backend failed to start. Check the logs above."
    exit 1
fi

echo ""
echo "🎨 Starting Frontend..."
cd ../frontend

# Install frontend dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Start frontend in background
echo "🚀 Starting frontend server on port 3000..."
npm start &
FRONTEND_PID=$!

# Wait for frontend to start
echo "⏳ Waiting for frontend to start..."
sleep 15

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend server is running on http://localhost:3000"
else
    echo "❌ Frontend failed to start. Check the logs above."
    exit 1
fi

echo ""
echo "🎉 Aivana is now running!"
echo "=================================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 To stop the services, press Ctrl+C"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for user to stop
echo "Press Ctrl+C to stop all services"
wait 