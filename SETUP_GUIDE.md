# 🚀 CoreAI Setup Guide

This guide will help you get CoreAI up and running in minutes.

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Node.js 18 or higher installed
- [ ] Python 3.9 or higher installed
- [ ] Git installed
- [ ] A Google AI API key (get from [Google AI Studio](https://aistudio.google.com/apikey))
- [ ] A Serper API key for search (get from [Serper.dev](https://serper.dev))

## ⚡ Quick Setup (5 minutes)

### Step 1: Clone and Navigate

```bash
git clone https://github.com/Tanaybaviskar/CoreAI.git
cd CoreAI
```

### Step 2: Backend Python Setup

```bash
# Navigate to Python backend
cd backend/agentic

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

**Edit `.env` file and add your API keys:**
```env
GOOGLE_API_KEY=your_google_ai_api_key
SERPER_API_KEY=your_serper_api_key
```

```bash
# Start Python server
python main.py
```

Keep this terminal running. The server should start on `http://localhost:5001`

### Step 3: Backend Node.js Proxy (New Terminal)

```bash
# From project root
cd backend

# Install dependencies
npm install

# Start proxy server
node index.js
```

Keep this terminal running. The server should start on `http://localhost:3001`

### Step 4: Frontend Setup (New Terminal)

```bash
# From project root
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend should start on `http://localhost:3000`

### Step 5: Open in Browser

Navigate to `http://localhost:3000` and start using CoreAI!

## 🎯 Getting Your API Keys

### 1. Google AI API Key (Required)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy the key to your `.env` file

### 2. Serper API Key (Required for Search)

1. Go to [Serper.dev](https://serper.dev)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy the key to your `.env` file

### 3. Optional APIs (For Extended Features)

#### Google Calendar & Gmail
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable APIs:
   - Google Calendar API
   - Gmail API
   - Google Meet API
4. Create credentials (API key or OAuth 2.0)
5. Add to `.env` file

#### Weather API
- **OpenWeatherMap**: [https://openweathermap.org/api](https://openweathermap.org/api)
- Free tier: 60 calls/minute

#### News API
- **NewsAPI**: [https://newsapi.org](https://newsapi.org)
- Free tier: 100 requests/day

## 🔍 Troubleshooting

### Port Already in Use

If you get "port already in use" errors:

```bash
# Find and kill the process
# Windows:
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:5001 | xargs kill -9
```

### Python Module Not Found

```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Build Errors

```bash
# Clear Next.js cache
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

### API Connection Errors

1. Check if all three servers are running:
   - Python: `http://localhost:5001/health`
   - Node.js: `http://localhost:3001/api/health`
   - Frontend: `http://localhost:3000`

2. Check `.env` file has valid API keys

3. Check firewall isn't blocking connections

## 📊 Verify Installation

Once all servers are running, test the setup:

1. **Health Check**:
   ```bash
   curl http://localhost:5001/health
   curl http://localhost:3001/api/health
   ```

2. **Frontend**: Open `http://localhost:3000`
   - You should see the CoreAI dashboard
   - Navigate to different pages
   - Try the chat interface

3. **Test Agent**: In the chat, type:
   ```
   What's the weather like today?
   ```
   The Weather Agent should respond with weather data.

## 🎨 First Steps

1. **Explore Dashboard**: See real-time statistics
2. **Visit Agents Page**: Check all 6 agents are running
3. **Try Chat**: Ask questions like:
   - "What's the weather today?"
   - "Show me my tasks"
   - "What's in the news?"
4. **Manage Connections**: Visit Connections page to see available integrations
5. **Customize Settings**: Set your name and AI persona

## 🚀 Production Deployment

### Environment Variables for Production

Create a production `.env` file:

```env
# Production settings
DEBUG=False
PORT=5001
HOST=0.0.0.0

# Your production API keys
GOOGLE_API_KEY=production_key_here
SERPER_API_KEY=production_key_here

# Security
SECRET_KEY=generate_a_secure_random_key
JWT_SECRET=generate_another_secure_key

# Database (if using)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Deployment Platforms

**Frontend (Vercel)**:
```bash
cd frontend
npm run build
vercel deploy --prod
```

**Backend (Railway)**:
1. Connect your GitHub repo
2. Add environment variables
3. Deploy from dashboard

## 📚 Next Steps

- Read the [full documentation](README.md)
- Explore the [agent system](backend/agentic/agents/)
- Customize the [frontend](frontend/src/app/)
- Add new agents
- Integrate more APIs

## 🆘 Need Help?

- Check [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Check existing issues for solutions

## ✅ Setup Complete!

You now have a fully functional enterprise AI assistant with:
- ✅ 6 specialized AI agents
- ✅ Supervisor coordination
- ✅ Modern web interface
- ✅ Real-time updates
- ✅ Multi-agent workflows

**Happy building! 🎉**
