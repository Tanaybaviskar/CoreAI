#!/bin/bash

# CoreAI Stop Script
# This script stops all CoreAI services

echo "🛑 Stopping CoreAI services..."

if [ -f ".pids" ]; then
    while IFS= read -r pid; do
        if ps -p $pid > /dev/null 2>&1; then
            echo "   Stopping process $pid..."
            kill $pid 2>/dev/null
        fi
    done < .pids
    rm .pids
    echo "✅ All services stopped"
else
    echo "⚠️  No PID file found. Attempting to stop by port..."

    # Kill processes on known ports
    if command -v lsof &> /dev/null; then
        lsof -ti:3000 | xargs kill -9 2>/dev/null
        lsof -ti:3001 | xargs kill -9 2>/dev/null
        lsof -ti:5001 | xargs kill -9 2>/dev/null
    elif command -v netstat &> /dev/null; then
        # Windows
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do taskkill /F /PID %%a 2>nul
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001') do taskkill /F /PID %%a 2>nul
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5001') do taskkill /F /PID %%a 2>nul
    fi

    echo "✅ Attempted to stop all services"
fi

echo ""
echo "🏁 CoreAI stopped"
