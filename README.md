# 🚀 CoreAI - Enterprise Multi-Agent AI Assistant

An enterprise-level AI assistant powered by a sophisticated multi-agent system. CoreAI coordinates specialized agents to handle your daily tasks including calendar management, email handling, meeting scheduling, weather updates, news aggregation, and task management.

![Enterprise AI](https://img.shields.io/badge/AI-Enterprise%20Grade-purple)
![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green)

## ✨ Features

### 🤖 Specialized AI Agents

- **📅 Calendar Agent**: Google Calendar integration for scheduling and availability checks
- **🎥 Meeting Agent**: Google Meet video conference management
- **📧 Email Agent**: Gmail operations - send, read, search, and organize
- **🌤️ Weather Agent**: Real-time weather data and forecasts
- **📰 News Agent**: News aggregation from multiple sources
- **✅ Task Agent**: Task and to-do list management

### 🎯 Supervisor Coordination

The Supervisor Agent intelligently:
- Routes requests to appropriate specialist agents
- Coordinates multi-step workflows (e.g., calendar check → meeting creation → calendar booking)
- Manages agent communication and data flow
- Provides unified response formatting

### 🎨 Enterprise Frontend

- **Modern Design**: Glassmorphism UI with animated gradients
- **Real-time Updates**: Live agent status monitoring
- **Responsive Dashboard**: Activity feeds and analytics
- **Multi-page Navigation**: Dashboard, Chat, Agents, Connections, Memory, Settings

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  Dashboard • Chat • Agents • Connections • Memory • Settings │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────┴──────────────────────────────────────┐
│                   Node.js Proxy Server                       │
│                      (Port 3001)                             │
└──────────────────────┬──────────────────────────────────────┘
                       │ Forward/Stream
┌──────────────────────┴──────────────────────────────────────┐
│              Python Flask Server (Port 5001)                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │            Supervisor Agent                        │    │
│  │  (Coordinates all specialist agents)               │    │
│  └──────┬──────────────────────────────────────┬──────┘    │
│         │                                       │            │
│  ┌──────┴───────┐  ┌──────────────┐  ┌────────┴──────┐    │
│  │  Calendar    │  │   Meeting    │  │    Email      │    │
│  │    Agent     │  │    Agent     │  │    Agent      │    │
│  └──────────────┘  └──────────────┘  └───────────────┘    │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐    │
│  │   Weather    │  │    News      │  │     Task      │    │
│  │    Agent     │  │    Agent     │  │     Agent     │    │
│  └──────────────┘  └──────────────┘  └───────────────┘    │
└────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/Tanaybaviskar/CoreAI.git
cd CoreAI
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend/agentic

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your API keys
# At minimum, you need:
# - GOOGLE_API_KEY (from Google AI Studio)
# - SERPER_API_KEY (for web search)
```

#### Start Python Server

```bash
python main.py
# Server will start on http://localhost:5001
```

### 3. Node.js Proxy Setup

```bash
cd ../../backend

# Install dependencies
npm install

# Start proxy server
node index.js
# Server will start on http://localhost:3001
```

### 4. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Frontend will start on http://localhost:3000
```

### 5. Access CoreAI

Open your browser to `http://localhost:3000`

## 🔑 API Keys & Integration

### Required APIs

1. **Google AI API** (Required)
   - Get from: https://aistudio.google.com/apikey
   - Used for: AI model (Gemini)

2. **Serper API** (Required for search)
   - Get from: https://serper.dev
   - Used for: Web search functionality

### Optional APIs (for full functionality)

3. **Google Calendar API**
   - Get from: https://console.cloud.google.com
   - Enable: Google Calendar API
   - Used for: Calendar management

4. **Gmail API**
   - Get from: https://console.cloud.google.com
   - Enable: Gmail API
   - Used for: Email operations

5. **Google Meet API**
   - Part of Google Workspace
   - Used for: Meeting creation

6. **Weather API**
   - Options: OpenWeatherMap, WeatherAPI
   - Get from: https://openweathermap.org/api
   - Used for: Weather information

7. **News API**
   - Get from: https://newsapi.org
   - Used for: News aggregation

## 📁 Project Structure

```
CoreAI/
├── frontend/                      # Next.js Frontend
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx          # Main application
│   │       ├── layout.tsx        # Root layout
│   │       └── globals.css       # Global styles
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                       # Node.js Proxy Server
│   ├── index.js                  # Express server
│   └── package.json
│
└── backend/agentic/              # Python Multi-Agent System
    ├── agents/                   # Agent implementations
    │   ├── base_agent.py        # Base agent class
    │   ├── supervisor.py        # Supervisor coordinator
    │   ├── calendar_agent.py    # Calendar operations
    │   ├── meeting_agent.py     # Meeting management
    │   ├── email_agent.py       # Email handling
    │   ├── task_agent.py        # Task management
    │   ├── info_agents.py       # Weather & News agents
    │   └── __init__.py
    ├── main.py                   # Flask server
    ├── requirements.txt          # Python dependencies
    └── .env.example             # Environment template
```

## 💡 Usage Examples

### Example 1: Schedule a Meeting

**You**: "Schedule a meeting for tomorrow at 2 PM"

**CoreAI**:
1. Calendar Agent checks availability for 2 PM
2. Meeting Agent creates Google Meet link
3. Calendar Agent books the time slot
4. Returns: Meeting link + Calendar confirmation

### Example 2: Check Weather & Read Emails

**You**: "What's the weather like and do I have any new emails?"

**CoreAI**:
1. Weather Agent fetches current weather
2. Email Agent checks inbox
3. Returns: Weather summary + Email list

### Example 3: Task Management

**You**: "Add a task to review the project proposal"

**CoreAI**:
1. Task Agent creates new task
2. Returns: Task confirmation with ID

## 🎨 Frontend Features

### Dashboard
- Real-time clock display
- Agent statistics (conversations, active agents, API calls, success rate)
- Recent activity feed
- Interactive stat cards

### Chat Interface
- Streaming responses
- Agent identification in messages
- Message history
- Real-time typing indicators

### Agents Page
- Live agent status monitoring
- Success rate visualization
- Last action display
- Performance metrics

### Connections
- API integration management
- Connection status indicators
- Quick connect/disconnect

### Memory
- Long-term memory storage
- Key-value pairs
- Editable entries

### Settings
- User profile customization
- AI persona selection
- System configuration
- Data management

## 🛠️ Technologies

### Frontend
- **Next.js 15** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling

### Backend (Python)
- **Flask** - Web framework
- **LangGraph** - Agent workflow orchestration
- **LangChain** - LLM framework
- **Google Gemini** - AI model

### Backend (Node.js)
- **Express** - Web server
- **Axios** - HTTP client
- **CORS** - Cross-origin support

## 🔒 Security Notes

- Never commit `.env` files with real API keys
- Use environment variables for all sensitive data
- Implement rate limiting in production
- Add authentication for deployed applications
- Use HTTPS in production

## 🚢 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel deploy
```

### Backend (Railway/Heroku)
```bash
# Deploy Python server
cd backend/agentic
# Follow your platform's deployment guide

# Deploy Node proxy
cd ../
# Follow your platform's deployment guide
```

## 📊 Performance

- **Response Time**: < 2s for most operations
- **Agent Coordination**: Parallel execution where possible
- **Streaming**: Real-time response streaming
- **Caching**: Intelligent API response caching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Google AI for Gemini API
- LangChain & LangGraph teams
- Next.js team
- Open source community

## 📧 Contact

For questions and support, please open an issue on GitHub.

---

**Built with ❤️ using cutting-edge AI technology**
