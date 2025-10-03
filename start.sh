#!/bin/bash

# AI Learn Programming Platform - Single Command Startup
# This script starts both backend and frontend together

echo "🚀 Starting AI Learn Programming Platform..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d ".venv" ] && [ ! -d "../.venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv ../.venv
    source ../.venv/bin/activate
    echo "📦 Installing dependencies..."
    pip install -r requirements-minimal.txt
else
    # Activate virtual environment
    if [ -d "../.venv" ]; then
        source ../.venv/bin/activate
    else
        source .venv/bin/activate
    fi
fi

echo ""
echo "✅ Environment ready!"
echo ""
echo "📡 Starting server on http://localhost:8000"
echo "   - Frontend: http://localhost:8000/"
echo "   - API Docs: http://localhost:8000/api/docs"
echo "   - API Health: http://localhost:8000/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the FastAPI server (serves both backend API and frontend)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
