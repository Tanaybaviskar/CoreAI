# 🏛️ CoreAI Architecture Documentation

This document explains the technical architecture of CoreAI's multi-agent system.

## 🎯 High-Level Overview

CoreAI implements a **hierarchical multi-agent system** where a Supervisor Agent coordinates multiple specialized agents to handle complex user requests.

```
User Request
     ↓
Supervisor Agent (Coordinator)
     ↓
[Analyzes Request & Routes to Agents]
     ↓
┌────────┬────────┬────────┬────────┬────────┬────────┐
↓        ↓        ↓        ↓        ↓        ↓        ↓
Calendar Meeting Email  Weather  News   Task
Agent    Agent    Agent   Agent   Agent  Agent
     ↓
[Executes Task]
     ↓
Returns Result to Supervisor
     ↓
Supervisor Formats Response
     ↓
User Receives Answer
```

## 🧩 Core Components

### 1. Base Agent Class

**File**: `backend/agentic/agents/base_agent.py`

The foundation for all specialized agents, providing:
- **Status Management**: idle, active, thinking, error
- **Performance Tracking**: Success/failure counts
- **Abstract Methods**: `execute()`, `can_handle()`

```python
class BaseAgent(ABC):
    def __init__(self, name, description)
    async def execute(task, context) -> Dict  # Implemented by subclasses
    def can_handle(task) -> bool              # Agent determines if it can handle task
    def update_status(status, action)
    def record_success() / record_failure()
    def get_success_rate() -> float
```

### 2. Specialized Agents

Each agent handles specific domain tasks:

#### Calendar Agent
**Purpose**: Manage calendar events and availability
**Capabilities**:
- Check free time slots
- Create calendar events
- List upcoming events
- Cancel/update events

**Keywords**: calendar, schedule, meeting, appointment, availability

#### Meeting Agent
**Purpose**: Create and manage video conferences
**Capabilities**:
- Generate Google Meet links
- Schedule video calls
- Provide meeting information

**Keywords**: meet, video call, conference, meeting link

#### Email Agent
**Purpose**: Gmail operations
**Capabilities**:
- Send emails
- Read inbox
- Search emails
- Create drafts

**Keywords**: email, mail, gmail, send, inbox, compose

#### Weather Agent
**Purpose**: Weather information
**Capabilities**:
- Current weather
- Multi-day forecast
- Weather alerts

**Keywords**: weather, temperature, forecast, rain, sunny

#### News Agent
**Purpose**: News aggregation
**Capabilities**:
- Latest headlines
- Category-specific news
- Article summaries

**Keywords**: news, headline, article, breaking news

#### Task Agent
**Purpose**: Task and to-do management
**Capabilities**:
- Add tasks
- Mark complete
- List tasks
- Delete tasks

**Keywords**: task, todo, reminder, checklist

### 3. Supervisor Agent

**File**: `backend/agentic/agents/supervisor.py`

The orchestrator that coordinates all agents.

#### Responsibilities

1. **Request Analysis**
   ```python
   async def process_request(user_message, context):
       # Analyzes the user's request
       # Determines which agents can handle it
   ```

2. **Agent Selection**
   ```python
   capable_agents = []
   for agent in self.agents:
       if agent.can_handle(user_message):
           capable_agents.append(agent)
   ```

3. **Execution Strategy**
   - **Single Agent**: Direct delegation
   - **Multiple Agents**: Coordinated workflow
   - **No Specific Agent**: General query handling

4. **Complex Workflows**
   ```python
   async def _coordinate_meeting_scheduling():
       # Step 1: Calendar Agent checks availability
       # Step 2: Meeting Agent creates link
       # Step 3: Calendar Agent books slot
   ```

## 🔄 Request Flow

### Simple Request Example: "What's the weather?"

```
1. User types: "What's the weather?"
2. Frontend sends to Node.js proxy (:3001)
3. Proxy forwards to Python Flask (:5001)
4. Supervisor receives request
5. Supervisor asks each agent: can_handle("What's the weather?")
6. Weather Agent responds: True
7. Supervisor delegates to Weather Agent
8. Weather Agent:
   - Updates status to "active"
   - Fetches weather data
   - Returns formatted result
9. Supervisor formats response
10. Flask streams response
11. Node.js proxy streams to frontend
12. Frontend displays result
```

### Complex Request Example: "Schedule a meeting for tomorrow at 2 PM"

```
1. User request arrives at Supervisor
2. Supervisor determines: Calendar + Meeting agents needed
3. Supervisor initiates workflow:

   Workflow Step 1: Calendar Agent
   - Task: Check availability for tomorrow 2 PM
   - Returns: Available time slots

   Workflow Step 2: Meeting Agent
   - Task: Create Google Meet link
   - Returns: Meeting link + ID

   Workflow Step 3: Calendar Agent
   - Task: Book the time slot with meeting link
   - Returns: Calendar event confirmation

4. Supervisor compiles results:
   - Meeting scheduled ✓
   - Calendar booked ✓
   - Meeting link generated ✓

5. Returns consolidated response to user
```

## 🗂️ Data Flow

### Frontend → Backend

```javascript
// Frontend sends
{
  "message": "Schedule a meeting",
  "thread_id": "thread_abc123",
  "context": {
    "date": "2024-03-20",
    "time": "14:00"
  }
}
```

### Backend Processing

```python
# Supervisor processes
supervisor.process_request(
    user_message="Schedule a meeting",
    context={"date": "2024-03-20", "time": "14:00"}
)

# Routes to agents
calendar_agent.execute(task, context)
meeting_agent.execute(task, context)
```

### Backend → Frontend

```json
{
  "success": true,
  "workflow": "meeting_scheduling",
  "steps": [
    {
      "step": 1,
      "agent": "Calendar Agent",
      "action": "check_availability",
      "result": {"success": true, "free_slots": [...]}
    },
    {
      "step": 2,
      "agent": "Meeting Agent",
      "action": "create_meeting",
      "result": {"success": true, "meeting_link": "..."}
    },
    {
      "step": 3,
      "agent": "Calendar Agent",
      "action": "book_slot",
      "result": {"success": true, "event_id": "..."}
    }
  ],
  "meeting_link": "https://meet.google.com/xyz",
  "message": "Meeting scheduled successfully"
}
```

## 🚀 Performance Optimizations

### 1. Parallel Agent Queries
When checking which agents can handle a request, all agents are queried simultaneously.

### 2. Streaming Responses
Responses stream to the frontend character-by-character for better UX.

### 3. Agent Status Caching
Agent status is tracked in memory for instant dashboard updates.

### 4. Async/Await
All agent operations use async/await for non-blocking execution.

## 🔒 Error Handling

### Agent-Level Errors
```python
try:
    result = await agent.execute(task, context)
    agent.record_success()
except Exception as e:
    agent.record_failure(str(e))
    return {"success": False, "error": str(e)}
```

### Supervisor-Level Recovery
- If primary agent fails, supervisor tries alternatives
- Graceful degradation to general query handling
- Error messages are user-friendly

## 📊 State Management

### Agent State
Each agent maintains:
- `status`: Current operational status
- `last_action`: Last performed action
- `success_count`: Successful operations
- `failure_count`: Failed operations

### Conversation History
Supervisor maintains:
```python
conversation_history = [
    {
        "timestamp": "2024-03-20T14:30:00",
        "role": "user",
        "content": "Schedule a meeting"
    },
    {
        "timestamp": "2024-03-20T14:30:05",
        "role": "assistant",
        "content": {"result": ...}
    }
]
```

## 🔌 Adding New Agents

To add a new agent:

1. **Create agent file**: `agents/your_agent.py`
2. **Inherit from BaseAgent**:
   ```python
   from .base_agent import BaseAgent

   class YourAgent(BaseAgent):
       def __init__(self):
           super().__init__(
               name="Your Agent",
               description="What it does"
           )

       def can_handle(self, task: str) -> bool:
           keywords = ["your", "keywords"]
           return any(k in task.lower() for k in keywords)

       async def execute(self, task: str, context: Dict) -> Dict:
           # Your implementation
           return {"success": True, "result": ...}
   ```

3. **Register in Supervisor**:
   ```python
   # agents/supervisor.py
   from .your_agent import YourAgent

   class SupervisorAgent:
       def __init__(self):
           self.agents = [
               ...,
               YourAgent(),  # Add here
           ]
   ```

4. **Import in __init__.py**:
   ```python
   # agents/__init__.py
   from .your_agent import YourAgent

   __all__ = [..., 'YourAgent']
   ```

## 🛠️ Technology Stack

### Backend Python
- **Flask**: Web framework
- **LangGraph**: Agent orchestration
- **LangChain**: LLM integration
- **Gemini**: AI model
- **asyncio**: Async operations

### Backend Node.js
- **Express**: HTTP server
- **Axios**: HTTP client
- **CORS**: Cross-origin support

### Frontend
- **Next.js**: React framework
- **TypeScript**: Type safety
- **Tailwind**: Styling

## 📈 Scalability Considerations

### Current Architecture
- Single-threaded Python with async
- In-memory state storage
- Suitable for: Single-user, development, demos

### Production Recommendations
- **Horizontal Scaling**: Deploy multiple instances
- **State Storage**: Redis for shared state
- **Database**: PostgreSQL for conversation history
- **Queue System**: Celery for long-running tasks
- **Load Balancer**: Nginx for distribution

## 🔮 Future Enhancements

1. **Agent Learning**: Track which agents work best for which queries
2. **Dynamic Agent Loading**: Load agents on-demand
3. **Agent Chaining**: More complex multi-step workflows
4. **Parallel Execution**: Run independent agents simultaneously
5. **Agent Marketplace**: Plugin system for community agents

## 📚 Related Documentation

- [Setup Guide](SETUP_GUIDE.md)
- [README](README.md)
- [API Documentation](backend/API.md)

---

**Last Updated**: March 2024
