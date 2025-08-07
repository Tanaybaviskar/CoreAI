@echo off
echo 🚀 Setting up CoreAI project...

REM Backend Node.js setup
echo 📦 Installing backend dependencies...
cd backend
call npm install

REM Frontend setup
echo 🎨 Installing frontend dependencies...
cd ..\frontend
call npm install

REM Python agentic setup
echo 🤖 Setting up Python environment...
cd ..\backend\agentic

REM Create virtual environment
python -m venv venv

echo ✅ Virtual environment created!
echo.
echo ⚠️  NEXT STEPS:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Install Python dependencies:
echo    pip install -r requirements.txt
echo.
echo 3. Copy .env.example to .env and add your Google AI API key:
echo    copy .env.example .env
echo    REM Edit .env and add your API key
echo.
echo 4. Run the agentic workflow:
echo    python main.py
echo.
echo 🎉 Setup complete! Check the README.md files for detailed instructions.
pause
