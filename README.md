# CoreAI

A full-stack AI-powered application with multi-agent workflows and modern web interface.

## 🏗️ Project Structure

```
CoreAI/
├── backend/
│   ├── agentic/          # Python multi-agent AI workflows
│   │   ├── main.py       # CrewAI workflow script
│   │   ├── requirements.txt
│   │   ├── .env          # API keys (create this)
│   │   └── README.md     # Agentic setup guide
│   ├── index.js          # Node.js backend
│   └── package.json      # Node.js dependencies
└── frontend/             # Next.js frontend application
    ├── src/
    ├── package.json
    └── README.md
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Tanaybaviskar/CoreAI.git
cd CoreAI
```

### 2. Backend Setup

#### Node.js Backend
```bash
cd backend
npm install
npm start
```

#### Python Agentic Workflow
```bash
cd backend/agentic
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# Create .env file with your Google AI API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

python main.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 🔑 Environment Setup

Create these environment files:

### `backend/agentic/.env`
```env
GOOGLE_API_KEY=your_google_ai_api_key_from_google_ai_studio
```

## 📚 Documentation

- **[Agentic Workflows](backend/agentic/README.md)** - Multi-agent AI system setup
- **[Frontend Guide](frontend/README.md)** - Next.js application setup
- **[Backend API](backend/)** - Node.js server documentation

## 🛠️ Technologies

- **Frontend**: Next.js, React, TypeScript
- **Backend**: Node.js, Express
- **AI/ML**: CrewAI, Google Gemini, LangChain
- **Deployment**: Ready for cloud deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
