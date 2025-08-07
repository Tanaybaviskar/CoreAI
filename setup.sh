#!/bin/bash

echo "🚀 Setting up CoreAI project..."

# Backend Node.js setup
echo "📦 Installing backend dependencies..."
cd backend
npm install

# Frontend setup
echo "🎨 Installing frontend dependencies..."
cd ../frontend
npm install

# Python agentic setup
echo "🤖 Setting up Python environment..."
cd ../backend/agentic

# Create virtual environment
python -m venv venv

# Activate virtual environment (instructions for user)
echo "✅ Virtual environment created!"
echo ""
echo "⚠️  NEXT STEPS:"
echo "1. Activate the virtual environment:"
echo "   Windows: venv\\Scripts\\activate"
echo "   macOS/Linux: source venv/bin/activate"
echo ""
echo "2. Install Python dependencies:"
echo "   pip install -r requirements.txt"
echo ""
echo "3. Copy .env.example to .env and add your Google AI API key:"
echo "   cp .env.example .env"
echo "   # Edit .env and add your API key"
echo ""
echo "4. Run the agentic workflow:"
echo "   python main.py"
echo ""
echo "🎉 Setup complete! Check the README.md files for detailed instructions."
