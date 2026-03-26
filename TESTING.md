# 🧪 Testing Your CoreAI Setup

Quick tests to verify everything is working correctly.

## 1. Health Checks

### Test Python Server
```bash
curl http://localhost:5001/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "CoreAI Multi-Agent System is running",
  "agents": [
    {"name": "Calendar Agent", "status": "idle", ...},
    {"name": "Meeting Agent", "status": "idle", ...},
    ...
  ],
  "total_agents": 6
}
```

### Test Node.js Proxy
```bash
curl http://localhost:3001/api/health
```

### Test Frontend
Open browser to `http://localhost:3000`

## 2. Test Individual Agents

### Test Weather Agent
```bash
curl -X POST http://localhost:5001/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather?", "thread_id": "test123"}'
```

### Test Task Agent
```bash
curl -X POST http://localhost:5001/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "Show my tasks", "thread_id": "test123"}'
```

### Test News Agent
```bash
curl -X POST http://localhost:5001/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "What is in the news?", "thread_id": "test123"}'
```

## 3. Test Through Frontend

### Test Basic Chat
1. Go to http://localhost:3000
2. Click on "Chat" in the sidebar
3. Type: "Hello, what can you do?"
4. You should get a response listing available agents

### Test Specific Agents

**Weather:**
- Type: "What's the weather today?"
- Expected: Weather Agent responds with temperature, conditions, forecast

**Tasks:**
- Type: "Show me my tasks"
- Expected: Task Agent lists current tasks

**News:**
- Type: "What's in the news?"
- Expected: News Agent shows latest headlines

**Calendar:**
- Type: "Check my calendar availability"
- Expected: Calendar Agent shows free time slots

## 4. Test Multi-Agent Workflow

Type: "Schedule a meeting for tomorrow at 2 PM"

**Expected Workflow:**
1. Supervisor identifies: Calendar + Meeting agents needed
2. Calendar Agent checks availability
3. Meeting Agent creates Google Meet link
4. Calendar Agent books the slot
5. Response includes all steps + meeting link

## 5. Test Dashboard Features

### View Agent Status
1. Navigate to "Agents" page
2. Check all 6 agents are shown
3. Verify status indicators (idle/active/thinking)
4. Check success rate percentages

### View Real-time Activity
1. Click the bell icon (top right)
2. Activity feed should appear
3. Make a request in chat
4. Activity should update

### Test Connections
1. Go to "Connections" page
2. Try toggling connections on/off
3. Status should update

## 6. Test Settings

1. Go to "Settings" page
2. Change your name
3. Select different AI persona
4. Click "Save Changes"
5. Return to Dashboard - greeting should use new name

## 7. Performance Tests

### Response Time Test
```bash
time curl -X POST http://localhost:5001/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather?", "thread_id": "test"}'
```

Should respond in < 2 seconds

### Concurrent Requests
Run multiple requests simultaneously:
```bash
for i in {1..5}; do
  curl -X POST http://localhost:5001/invoke \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Test $i\", \"thread_id\": \"test$i\"}" &
done
wait
```

All should complete successfully

## 8. Error Handling Tests

### Invalid Request
```bash
curl -X POST http://localhost:5001/invoke \
  -H "Content-Type: application/json" \
  -d '{"thread_id": "test"}'
```
Should return error: "Message is required"

### Unavailable Agent
Type in chat: "xyzabc123nonsense"
Should get general response from Supervisor

## 9. Browser Console Tests

Open browser DevTools (F12), go to Console:

### Test API Connection
```javascript
fetch('http://localhost:3001/api/health')
  .then(r => r.json())
  .then(d => console.log('Health:', d))
```

### Test Chat API
```javascript
fetch('http://localhost:3001/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'Test message',
    thread_id: 'browser-test'
  })
}).then(r => r.text()).then(console.log)
```

## 10. Logs Check

### View Python Logs
```bash
# If using start.sh/start.bat
cat logs/python.log    # Unix
type logs\python.log   # Windows

# Or check the console where Python is running
```

Look for:
- ✓ "CoreAI Multi-Agent System is running"
- ✓ No error stack traces
- ✓ Agent initialization messages

### View Node.js Logs
```bash
cat logs/nodejs.log    # Unix
type logs\nodejs.log   # Windows
```

Look for:
- ✓ "Node.js server listening at http://localhost:3001"
- ✓ No connection errors

### View Frontend Logs
```bash
cat logs/frontend.log   # Unix
type logs\frontend.log  # Windows
```

Look for:
- ✓ "Ready on http://localhost:3000"
- ✓ No compilation errors

## ✅ Success Checklist

After testing, you should have:

- [ ] All 3 servers running without errors
- [ ] Health endpoints responding
- [ ] Frontend loads and displays dashboard
- [ ] Chat interface accepts and responds to messages
- [ ] At least 3 different agents tested successfully
- [ ] Dashboard showing real-time data
- [ ] Agent status page showing all 6 agents
- [ ] No error messages in browser console
- [ ] No error messages in server logs

## 🐛 Common Issues

### "Port already in use"
```bash
# Stop all services
./stop.sh   # or stop.bat on Windows

# Then restart
./start.sh  # or start.bat on Windows
```

### "Module not found" (Python)
```bash
cd backend/agentic
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### "Cannot find module" (Node.js)
```bash
cd backend
npm install

cd ../frontend
npm install
```

### Frontend not loading
- Check if port 3000 is available
- Check browser console for errors
- Verify backend servers are running
- Try clearing Next.js cache: `rm -rf frontend/.next`

### API Key Errors
- Verify `.env` file exists in `backend/agentic/`
- Check API keys are valid
- Ensure no extra spaces or quotes in .env

## 🎉 All Tests Pass?

Congratulations! Your CoreAI system is fully operational.

Next steps:
- Explore different agent capabilities
- Try complex multi-step requests
- Customize the frontend design
- Add your own agents
- Integrate real APIs (Google Calendar, Gmail, etc.)

Happy building! 🚀
