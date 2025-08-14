#!/bin/bash

echo "🚀 Starting Enoxify with Authentication..."

# Kill any existing processes
echo "🔄 Stopping existing processes..."
pkill -f "python main_with_auth.py" 2>/dev/null
pkill -f "python main.py" 2>/dev/null
pkill -f "python simple_test_main.py" 2>/dev/null

# Wait a moment for processes to stop
sleep 2

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found in backend directory!"
    echo "📝 Please copy env_template.txt to .env and add your OpenAI API key and JWT secret"
    echo "   cp backend/env_template.txt backend/.env"
    echo "   Then edit backend/.env with your actual values"
    exit 1
fi

# Start backend with authentication
echo "🔧 Starting backend with authentication..."
cd backend
source venv/bin/activate
echo "✅ Backend virtual environment activated"
echo "🚀 Starting Enoxify backend on http://localhost:8000"
echo "📚 API docs available at http://localhost:8000/docs"
echo "🔐 Authentication endpoints:"
echo "   - POST /auth/signup - Create account"
echo "   - POST /auth/login - Sign in"
echo "   - GET /auth/me - Get user info"
echo ""
echo "Press Ctrl+C to stop the backend"
echo ""

python main_with_auth.py 