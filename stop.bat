@echo off
REM CoreAI Stop Script for Windows

echo Stopping CoreAI services...
echo.

REM Force stop port 5000 (Backend FIXED port)
echo Checking port 5000 (Backend)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do (
    echo Stopping backend process on port 5000 (PID %%a)
    taskkill /F /PID %%a >nul 2>&1
)

REM Force stop port 3001 (Node.js Proxy)
echo Checking port 3001 (Proxy)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001 ^| findstr LISTENING') do (
    echo Stopping proxy process on port 3001 (PID %%a)
    taskkill /F /PID %%a >nul 2>&1
)

REM Stop any other backend ports (cleanup)
for %%p in (5001 5002 5003 5004 5005) do (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%%p ^| findstr LISTENING') do (
        echo Stopping stray backend process on port %%p (PID %%a)
        taskkill /F /PID %%a >nul 2>&1
    )
)

REM Stop frontend ports
for %%p in (3000 3001 3002 3003 3004 3005 3006 3007 3008 3009 3010) do (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%%p ^| findstr LISTENING') do (
        echo Stopping frontend process on port %%p (PID %%a)
        taskkill /F /PID %%a >nul 2>&1
    )
)

echo.
echo All CoreAI services stopped - Port 5000 is now free for backend
echo.
timeout /t 2 /nobreak >nul
