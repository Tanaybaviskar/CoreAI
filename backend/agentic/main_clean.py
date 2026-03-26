"""
CoreAI Multi-Agent System
Enterprise-level AI assistant powered by specialized agents
"""
from flask import Flask, request, jsonify, Response, redirect, session, url_for
from flask_cors import CORS
import json
import asyncio
from dotenv import load_dotenv
import os
import socket
from datetime import datetime
import secrets

from agents.supervisor import SupervisorAgent
from utils.oauth_helper import GoogleOAuthHelper

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Set secret key for sessions
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Initialize OAuth helper
oauth_helper = GoogleOAuthHelper()

# Initialize the Supervisor Agent (coordinates all specialized agents)
supervisor = SupervisorAgent()

def find_available_port(start_port=5000, max_attempts=100):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('0.0.0.0', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

print("=" * 60)
print(">> CoreAI Multi-Agent System Starting...")
print("=" * 60)
print("\n>> Available Agents:")
for agent in supervisor.agents:
    print(f"   * {agent.name}: {agent.description}")
print("\n" + "=" * 60)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    agents_status = supervisor.get_all_agents_status()

    return jsonify({
        "status": "ok",
        "message": "CoreAI Multi-Agent System is running",
        "timestamp": datetime.now().isoformat(),
        "agents": agents_status,
        "total_agents": len(supervisor.agents)
    })


@app.route('/invoke', methods=['POST'])
def invoke_agent():
    """Main chat endpoint - processes requests through the supervisor"""
    try:
        data = request.get_json()
        message = data.get('message')
        thread_id = data.get('thread_id', 'default')
        context = data.get('context', {})

        if not message:
            return jsonify({"error": "Message is required"}), 400

        def generate():
            """Stream response"""
            try:
                # Process through supervisor agent
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(
                    supervisor.process_request(message, context)
                )
                loop.close()

                # Format response for streaming
                response_text = format_agent_response(result)

                # Stream the response
                for char in response_text:
                    yield char

            except Exception as e:
                error_msg = f"\n\n[!] Error: {str(e)}"
                yield error_msg

        return Response(generate(), mimetype='text/plain')

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get dashboard analytics data"""
    agents_status = supervisor.get_all_agents_status()

    # Calculate aggregate statistics
    total_tasks = sum(agent['total_tasks'] for agent in agents_status)
    avg_success_rate = sum(agent['success_rate'] for agent in agents_status) / len(agents_status) if agents_status else 0
    active_agents = sum(1 for agent in agents_status if agent['status'] == 'active')

    recent_activity = [
        {
            "time": "2 min ago",
            "action": f"{agents_status[0]['name']} completed task",
            "status": "success",
            "type": "success"
        },
        {
            "time": "5 min ago",
            "action": "New API connection established",
            "status": "info",
            "type": "info"
        },
        {
            "time": "12 min ago",
            "action": f"{agents_status[1]['name']} is processing request",
            "status": "info",
            "type": "info"
        }
    ] if agents_status else []

    return jsonify({
        "totalConversations": len(supervisor.conversation_history) // 2,
        "activeAgents": active_agents,
        "apiCallsToday": total_tasks,
        "successRate": round(avg_success_rate, 1),
        "recentActivity": recent_activity
    })


@app.route('/agents', methods=['GET'])
def get_agents():
    """Get all agents and their status"""
    agents_status = supervisor.get_all_agents_status()
    return jsonify({
        "agents": agents_status,
        "total": len(agents_status)
    })


@app.route('/agents/<agent_name>', methods=['GET'])
def get_agent_info(agent_name):
    """Get specific agent information"""
    agent = supervisor.get_agent_by_name(agent_name)
    if agent:
        return jsonify(agent.get_info())
    return jsonify({"error": "Agent not found"}), 404


@app.route('/memory', methods=['GET', 'POST'])
def manage_memory():
    """Manage agent memory/knowledge base"""
    if request.method == 'GET':
        return jsonify({
            "memory_items": [
                {"id": "1", "key": "User Preference", "value": "Prefers detailed explanations"},
                {"id": "2", "key": "Project Context", "value": "Working on CoreAI multi-agent system"},
                {"id": "3", "key": "Communication Style", "value": "Professional and concise"},
                {"id": "4", "key": "Timezone", "value": "UTC"},
            ]
        })
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({"status": "Memory item added", "data": data})


@app.route('/settings', methods=['GET', 'POST'])
def manage_settings():
    """Manage system settings"""
    if request.method == 'GET':
        return jsonify({
            "model": "gemini-2.0-flash",
            "temperature": 0.7,
            "max_tokens": 4000,
            "enable_search": True,
            "enable_multi_agent": True,
            "agents_enabled": [agent.name for agent in supervisor.agents]
        })
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({"status": "Settings updated", "data": data})


@app.route('/activity', methods=['GET'])
def get_activity():
    """Get recent activity log"""
    # Get recent conversation history
    recent_conversations = supervisor.conversation_history[-10:]

    activities = []
    for conv in recent_conversations:
        time = datetime.fromisoformat(conv['timestamp']).strftime("%I:%M %p")
        if conv['role'] == 'user':
            text = f"User: {conv['content'][:50]}..."
        else:
            text = f"Assistant completed request"

        activities.append({
            "time": time,
            "text": text
        })

    return jsonify({"activities": activities})


# ============================================================================
# OAUTH ENDPOINTS
# ============================================================================

@app.route('/auth/status', methods=['GET'])
def auth_status():
    """Check if user is logged in"""
    user_email = session.get('user_email')
    if user_email and oauth_helper.get_user_session(user_email):
        user_data = oauth_helper.get_user_session(user_email)
        return jsonify({
            'authenticated': True,
            'user': user_data['user_info'],
            'scopes': user_data.get('scopes', [])
        })
    else:
        return jsonify({
            'authenticated': False,
            'oauth_configured': oauth_helper.is_configured()
        })


@app.route('/auth/login', methods=['GET'])
def auth_login():
    """Initiate Google OAuth login"""
    if not oauth_helper.is_configured():
        return jsonify({'error': 'OAuth not configured'}), 400

    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    auth_url = oauth_helper.get_authorization_url(state=state)
    if not auth_url:
        return jsonify({'error': 'Failed to generate auth URL'}), 500

    return jsonify({'auth_url': auth_url})


@app.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    """Handle OAuth callback"""
    # Verify state parameter
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return "Invalid state parameter", 400

    # Get authorization code
    code = request.args.get('code')
    if not code:
        error = request.args.get('error')
        return f"OAuth error: {error}", 400

    # Exchange code for tokens
    token_data = oauth_helper.exchange_code_for_tokens(code)
    if not token_data:
        return "Failed to exchange code for tokens", 500

    # Store user session
    user_email = token_data['user_info']['email']
    session['user_email'] = user_email

    # Clean up OAuth state
    session.pop('oauth_state', None)

    # Get the frontend port dynamically (since it auto-selects now)
    frontend_url = request.host_url.replace(':500', ':300')  # Assume frontend is on 300x range
    return redirect(f"{frontend_url}?auth=success")


@app.route('/auth/logout', methods=['POST'])
def auth_logout():
    """Logout user and revoke tokens"""
    user_email = session.get('user_email')
    if user_email:
        oauth_helper.revoke_user_session(user_email)
        session.pop('user_email', None)
        return jsonify({'message': 'Logged out successfully'})
    else:
        return jsonify({'error': 'Not logged in'}), 400


@app.route('/auth/users', methods=['GET'])
def get_logged_in_users():
    """Get all logged-in users (for admin/debug)"""
    users = oauth_helper.get_all_logged_in_users()
    return jsonify({'users': users, 'count': len(users)})


def format_agent_response(result: dict) -> str:
    """Format agent response for user-friendly display"""
    if not result.get("success", False):
        return f"[!] {result.get('message', 'An error occurred')}"

    # Handle different response types
    if "workflow" in result:
        # Complex multi-agent workflow
        response = f"[OK] {result.get('message', 'Task completed')}\n\n"
        response += ">> Workflow Steps:\n"
        for step in result.get('steps', []):
            response += f"  {step['step']}. {step['agent']}: {step['result'].get('message', 'Completed')}\n"

        if result.get('meeting_link'):
            response += f"\n>> Meeting Link: {result['meeting_link']}"

        return response

    elif "result" in result:
        # Single agent result
        inner_result = result['result']
        response = f">> {result.get('agent', 'Agent')}\n\n"

        # Handle specific agent results
        if inner_result.get('action') == 'check_availability':
            response += f">> {inner_result.get('message')}\n\n"
            if inner_result.get('free_slots'):
                response += "Available time slots:\n"
                for slot in inner_result['free_slots']:
                    response += f"  • {slot['start']} - {slot['end']}\n"

        elif inner_result.get('action') == 'get_weather':
            current = inner_result.get('current', {})
            response += f"{inner_result.get('message')}\n\n"
            response += f"Humidity: {current.get('humidity')}% | Wind: {current.get('wind_speed')} km/h\n\n"
            if inner_result.get('forecast'):
                response += "Forecast:\n"
                for day in inner_result['forecast']:
                    response += f"  • {day['day']}: {day['high']}°/{day['low']}° - {day['condition']}\n"

        elif inner_result.get('action') == 'get_news':
            response += f">> {inner_result.get('message')}\n\n"
            if inner_result.get('articles'):
                for i, article in enumerate(inner_result['articles'][:3], 1):
                    response += f"{i}. {article['title']}\n"
                    response += f"   {article['source']} - {article['description'][:100]}...\n\n"

        elif inner_result.get('action') == 'read_emails':
            response += f">> {inner_result.get('message')}\n\n"
            if inner_result.get('emails'):
                for email in inner_result['emails']:
                    unread = "[UNREAD] " if email.get('unread') else ""
                    response += f"{unread}{email['subject']}\n"
                    response += f"   From: {email['from']} - {email['snippet'][:80]}...\n\n"

        elif inner_result.get('action') == 'list_tasks':
            response += f">> {inner_result.get('message')}\n\n"
            if inner_result.get('tasks'):
                for task in inner_result['tasks']:
                    priority = {"high": "[HIGH]", "medium": "[MED]", "low": "[LOW]"}.get(task.get('priority', 'medium'), "[?]")
                    response += f"{priority} {task['title']}\n"

        else:
            response += inner_result.get('message', 'Task completed successfully')

        return response

    else:
        # General message
        return result.get('message', 'Task completed')


if __name__ == "__main__":
    # Find available port
    port = find_available_port(5000)
    if not port:
        print("[ERROR] Could not find available port!")
        exit(1)

    print("\n>> Server Configuration:")
    print(f"   Host: 0.0.0.0")
    print(f"   Port: {port}")
    print(f"   Mode: {'Debug' if os.getenv('DEBUG', 'True') == 'True' else 'Production'}")
    print("\n>> Available Endpoints:")
    print("   GET  /health      - System health check")
    print("   POST /invoke      - Process user request")
    print("   GET  /dashboard   - Get dashboard data")
    print("   GET  /agents      - Get all agents status")
    print("   GET  /memory      - Get memory items")
    print("   GET  /settings    - Get system settings")
    print("   GET  /activity    - Get activity log")
    print("   GET  /auth/*      - OAuth endpoints")
    print("\n" + "=" * 60)
    print(f">> CoreAI is ready! Backend running on: http://localhost:{port}")
    print("=" * 60 + "\n")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('DEBUG', 'True') == 'True',
        threaded=True
    )