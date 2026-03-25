from typing import Annotated
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
import os
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool, InjectedToolCallId, Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import threading
import time

from langchain_core.messages import ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from langgraph.types import Command, interrupt
from langgraph.prebuilt import tools_condition

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}



class State(TypedDict):
    messages: Annotated[list, add_messages]
    name: str
    birthday: str


# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

search = GoogleSerperAPIWrapper()
llm = init_chat_model("google_genai:gemini-2.0-flash")



graph_builder = StateGraph(State)

@tool
def human_assistance( name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]
) -> str:
    """Request assistance from a human."""
    human_response = interrupt(
        {
            "question": "Is this correct?",
            "name": name,
            "birthday": birthday,
        },
    )
    # If the information is correct, update the state as-is.
    if human_response.get("correct", "").lower().startswith("y"):
        verified_name = name
        verified_birthday = birthday
        response = "Correct"
    # Otherwise, receive information from the human reviewer.
    else:
        verified_name = human_response.get("name", name)
        verified_birthday = human_response.get("birthday", birthday)
        response = f"Made a correction: {human_response}"
    # This time we explicitly update the state with a ToolMessage inside
    # the tool.
    state_update = {
        "name": verified_name,
        "birthday": verified_birthday,
        "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
    }
    # We return a Command object in the tool to update our state.
    return Command(update=state_update)



tools = [
    Tool(
        name="Intermediate_Answer",
        func=search.run,
        description="useful for when you need to ask with search",
    ), 
    human_assistance
]

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1
    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)


tool_node = BasicToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

def route_tools(
    state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)



def stream_graph_updates(user_input: str, thread_id: str = "1"):
    """Stream graph updates for a given user input and thread ID"""
    config = {"configurable": {"thread_id": thread_id}}
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )

    for event in events:
        if "messages" in event:
            message = event["messages"][-1]
            yield f"data: {json.dumps({'content': message.content, 'type': 'message'})}\n\n"

# Flask API Endpoints
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "message": "CoreAI Python Agent is running",
        "models": ["gemini-2.0-flash"],
        "capabilities": ["web_search", "human_in_loop", "multi_agent"]
    })

@app.route('/invoke', methods=['POST'])
def invoke_agent():
    """Main chat endpoint that streams responses"""
    try:
        data = request.get_json()
        message = data.get('message')
        thread_id = data.get('thread_id', 'default')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        def generate():
            try:
                for update in stream_graph_updates(message, thread_id):
                    yield update
                    time.sleep(0.1)  # Small delay for better streaming
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e), 'type': 'error'})}\n\n"
        
        return Response(generate(), mimetype='text/plain')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get dashboard analytics data"""
    return jsonify({
        "total_conversations": 1247,
        "active_agents": 3,
        "api_calls_today": 3421,
        "success_rate": 97.8,
        "recent_activity": [
            {"time": "2 min ago", "action": "Research Agent completed web search", "status": "success"},
            {"time": "5 min ago", "action": "New connection added", "status": "info"},
            {"time": "12 min ago", "action": "Human assistance requested", "status": "warning"}
        ]
    })

@app.route('/memory', methods=['GET', 'POST'])
def manage_memory():
    """Manage agent memory/knowledge base"""
    if request.method == 'GET':
        # Return current memory items
        return jsonify({
            "memory_items": [
                {"id": "1", "key": "User Preference", "value": "Prefers detailed explanations"},
                {"id": "2", "key": "Project Context", "value": "Working on CoreAI system"}
            ]
        })
    elif request.method == 'POST':
        # Add new memory item
        data = request.get_json()
        # In a real implementation, you'd save this to a database
        return jsonify({"status": "Memory item added", "data": data})

@app.route('/settings', methods=['GET', 'POST'])
def manage_settings():
    """Manage agent settings"""
    if request.method == 'GET':
        return jsonify({
            "model": "gemini-2.0-flash",
            "temperature": 0.7,
            "max_tokens": 4000,
            "enable_search": True,
            "enable_human_loop": True
        })
    elif request.method == 'POST':
        data = request.get_json()
        # In a real implementation, you'd save settings
        return jsonify({"status": "Settings updated", "data": data})

@app.route('/activity', methods=['GET'])
def get_activity():
    """Get recent activity log"""
    return jsonify({
        "activities": [
            {"time": "10:15 AM", "text": "User asked about LangGraph architecture"},
            {"time": "9:30 AM", "text": "Web search performed for AI agents"},
            {"time": "9:00 AM", "text": "System initialized successfully"}
        ]
    })

if __name__ == "__main__":
    # You can still run the CLI version for testing
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Command line interface mode
        print("CoreAI CLI Mode - Type 'quit' to exit")
        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break

                for update in stream_graph_updates(user_input):
                    print(update.replace("data: ", "").replace("\n\n", ""))
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                break
    else:
        # Web server mode (default)
        print("🚀 Starting CoreAI Agent Server...")
        print("📡 Server will run on http://localhost:5001")
        print("🔗 Connect your frontend to this endpoint")
        print("⚡ Available endpoints:")
        print("   GET  /health - Health check")
        print("   POST /invoke - Chat with AI agent")
        print("   GET  /dashboard - Analytics data")
        print("   GET/POST /memory - Memory management")
        print("   GET/POST /settings - Settings management")
        print("   GET  /activity - Activity log")
        
        app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)



