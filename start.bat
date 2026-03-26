@echo off
REM CoreAI Startup Script for Windows

echo ========================================
echo Starting CoreAI Multi-Agent System...
echo ========================================
echo.

REM Create logs directory
if not exist "logs" mkdir logs

REM Start Python backend
echo 1. Starting Python Agent Server (Prefers Port 5000)...
cd backend\agentic

REM Check if virtual environment exists
if not exist "venv" (
    echo Warning: Virtual environment not found. Creating...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Check if .env exists
if not exist ".env" (
    echo Warning: .env file not found. Creating from .env.example...
    copy .env.example .env
    echo Warning: Please edit backend\agentic\.env and add your API keys!
    pause
)

REM Start Python server in new window
start "CoreAI - Python Backend" cmd /k "venv\Scripts\activate && python main.py"
echo Backend server starting...
echo.

cd ..\..

REM Wait for Python server
echo Waiting for backend server...
timeout /t 3 /nobreak >nul

REM Start Node.js proxy
echo 2. Starting Node.js Proxy Server (Port 3001)...
cd backend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Warning: node_modules not found. Installing...
    call npm install
)

REM Start Node.js server in new window
start "CoreAI - Node.js Proxy" cmd /k "node index.js"
echo Proxy server starting...
echo.

cd ..

REM Wait for proxy server
echo Waiting for proxy server...
timeout /t 2 /nobreak >nul

REM Start Frontend
echo 3. Starting Next.js Frontend (Auto Port Detection)...
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Warning: node_modules not found. Installing...
    call npm install
)

REM Start frontend in new window
start "CoreAI - Frontend" cmd /k "npm run dev"
echo Frontend starting...
echo.

cd ..

echo.
echo ========================================
echo CoreAI is starting up!
echo ========================================
echo.
echo Services:
echo    • Backend Server:  http://localhost:5000 (Python backend)
echo    • Proxy Server:    http://localhost:3001 (Node.js proxy)
echo    • Frontend:        Auto-detected port (typically 3000-3010)
echo.
echo Waiting for services to be fully ready...
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo CoreAI is ready!
echo ========================================
echo.
echo Check the service windows for actual ports used.
echo Frontend will show its port in its startup window.
echo.
echo Three command windows will remain open for each service.
echo Close them to stop the services, or run stop.bat
echo.
pause
