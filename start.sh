#!/bin/bash

# CoreAI Startup Script
# This script starts all CoreAI services

echo "🚀 Starting CoreAI Multi-Agent System..."
echo "========================================="

# Check if running on Windows (Git Bash or WSL)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    PYTHON_CMD="python"
    VENV_ACTIVATE="venv/Scripts/activate"
else
    PYTHON_CMD="python3"
    VENV_ACTIVATE="venv/bin/activate"
fi

# Function to check if a port is in use
check_port() {
    if command -v lsof &> /dev/null; then
        lsof -ti:$1 &> /dev/null
    elif command -v netstat &> /dev/null; then
        netstat -ano | grep ":$1" &> /dev/null
    else
        return 1
    fi
}

# Function to kill process on port
kill_port() {
    echo "⚠️  Port $1 is in use, attempting to free it..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :$1') do taskkill /F /PID %%a 2>nul
    else
        # Unix-like
        lsof -ti:$1 | xargs kill -9 2>/dev/null
    fi
}

# Check and clean ports
echo ""
echo "🔍 Checking ports..."
if check_port 3000; then
    kill_port 3000
fi
if check_port 3001; then
    kill_port 3001
fi
if check_port 5001; then
    kill_port 5001
fi

echo "✅ Ports are ready"
echo ""

# Start Python backend
echo "1️⃣  Starting Python Agent Server (Port 5001)..."
cd backend/agentic

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    $PYTHON_CMD -m venv venv
    source $VENV_ACTIVATE
    pip install -r requirements.txt
else
    source $VENV_ACTIVATE
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit backend/agentic/.env and add your API keys!"
    echo "Press Enter to continue anyway or Ctrl+C to cancel..."
    read
fi

# Start Python server in background
$PYTHON_CMD main.py > ../../logs/python.log 2>&1 &
PYTHON_PID=$!
echo "✅ Python server started (PID: $PYTHON_PID)"

cd ../..

# Wait for Python server to be ready
echo "⏳ Waiting for Python server..."
sleep 3

# Start Node.js proxy
echo ""
echo "2️⃣  Starting Node.js Proxy Server (Port 3001)..."
cd backend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found. Installing..."
    npm install
fi

# Start Node.js server in background
node index.js > ../logs/nodejs.log 2>&1 &
NODEJS_PID=$!
echo "✅ Node.js proxy started (PID: $NODEJS_PID)"

cd ..

# Wait for Node.js server to be ready
echo "⏳ Waiting for Node.js proxy..."
sleep 2

# Start Frontend
echo ""
echo "3️⃣  Starting Next.js Frontend (Port 3000)..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  node_modules not found. Installing..."
    npm install
fi

# Start frontend in background
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID)"

cd ..

# Create logs directory if it doesn't exist
mkdir -p logs

# Summary
echo ""
echo "========================================="
echo "✨ CoreAI is starting up!"
echo "========================================="
echo ""
echo "📡 Services:"
echo "   • Python Agent Server:  http://localhost:5001"
echo "   • Node.js Proxy:        http://localhost:3001"
echo "   • Frontend:             http://localhost:3000"
echo ""
echo "📋 Process IDs:"
echo "   • Python:    $PYTHON_PID"
echo "   • Node.js:   $NODEJS_PID"
echo "   • Frontend:  $FRONTEND_PID"
echo ""
echo "📝 Logs:"
echo "   • View logs in the ./logs/ directory"
echo "   • Python:    logs/python.log"
echo "   • Node.js:   logs/nodejs.log"
echo "   • Frontend:  logs/frontend.log"
echo ""
echo "⏳ Waiting for services to be fully ready..."
sleep 5

# Health check
echo ""
echo "🏥 Health Check:"
if curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo "   ✅ Python server is healthy"
else
    echo "   ⚠️  Python server not responding (check logs/python.log)"
fi

if curl -s http://localhost:3001/api/health > /dev/null 2>&1; then
    echo "   ✅ Node.js proxy is healthy"
else
    echo "   ⚠️  Node.js proxy not responding (check logs/nodejs.log)"
fi

echo ""
echo "========================================="
echo "🎉 CoreAI is ready!"
echo "========================================="
echo ""
echo "🌐 Open your browser to: http://localhost:3000"
echo ""
echo "To stop all services, run: ./stop.sh"
echo "Or press Ctrl+C to keep services running in background"
echo ""

# Save PIDs to file for stop script
echo "$PYTHON_PID" > .pids
echo "$NODEJS_PID" >> .pids
echo "$FRONTEND_PID" >> .pids

# Keep script running
wait
