# 🚀 Quick Start - Running CoreAI

## ✅ You Already Have

Your `.env` file is configured with:
- ✅ **GOOGLE_API_KEY** - Core AI functionality
- ✅ **SERPER_API_KEY** - Web search capability

**This is enough to run the app right now!**

---

## 🎯 Start CoreAI (3 Easy Steps)

### **Windows:**
```bash
# Just run this from CoreAI root directory:
start.bat
```

### **Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### **Manual Start:**
```bash
# Terminal 1 - Python Backend
cd backend/agentic
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python main.py

# Terminal 2 - Node.js Proxy
cd backend
npm install
node index.js

# Terminal 3 - Frontend
cd frontend
npm install
npm run dev
```

---

## 🌐 Access Your App

Open browser to: **http://localhost:3000**

---

## 🎨 What Works Right Now

All agents work with **simulated data**:

- ✅ **Chat Interface** - Full AI conversation
- ✅ **Calendar Agent** - Simulated calendar events
- ✅ **Meeting Agent** - Simulated meeting links
- ✅ **Email Agent** - Simulated emails
- ✅ **Weather Agent** - Simulated weather data
- ✅ **News Agent** - Simulated news articles
- ✅ **Task Agent** - Real task management (in-memory)

---

## 🔑 Want Real API Data?

### Phase 1: Essential (Get these first)

Follow [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) to add:

1. **Google OAuth 2.0** ⭐ Most Important
   - Real Calendar access
   - Real Gmail access
   - Real meeting creation
   - **Time:** ~15 minutes
   - **Free:** Yes

2. **Weather API** (OpenWeatherMap)
   - Real weather data
   - **Time:** ~5 minutes
   - **Free:** Yes (60 calls/min)

3. **News API**
   - Real news headlines
   - **Time:** ~5 minutes
   - **Free:** Yes (100 calls/day)

### Phase 2: Optional (Add later if needed)

- Slack Integration
- Microsoft Teams
- Notion
- Trello
- Discord

---

## 📖 Documentation Quick Links

| Document | Purpose | When to Read |
|----------|---------|--------------|
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Initial setup steps | Before starting |
| [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) | OAuth & API keys | When adding real APIs |
| [TESTING.md](TESTING.md) | Test everything | After setup |
| [ARCHITECTURE.md](ARCHITECTURE.md) | How it works | For developers |
| [README.md](README.md) | Full overview | Anytime |

---

## 🧪 Quick Test

After starting, try these in the chat:

```
What's the weather like?
Show me my tasks
What's in the news?
Schedule a meeting for tomorrow
```

---

## 🛑 Stop the App

```bash
stop.bat      # Windows
./stop.sh     # Mac/Linux
```

Or just close the terminal windows.

---

## 💡 Pro Tips

1. **Start with what you have** - The app is fully functional right now with simulated data!

2. **Add APIs gradually:**
   - Day 1: Just run it with simulated data
   - Day 2: Add Google OAuth for real Calendar/Gmail
   - Day 3: Add Weather + News APIs
   - Later: Add optional integrations

3. **Common Commands:**
   ```bash
   # Check if servers are running
   curl http://localhost:5001/health  # Python
   curl http://localhost:3001/api/health  # Node.js

   # View logs (if using start.sh/bat)
   cat logs/python.log
   cat logs/nodejs.log
   cat logs/frontend.log
   ```

4. **Stuck?** Check [TESTING.md](TESTING.md) troubleshooting section

---

## 🎉 You're Ready!

The app is production-ready to start right now. Add real APIs later when you need them.

**Questions?** See the docs or open an issue on GitHub.

Happy building! 🚀
