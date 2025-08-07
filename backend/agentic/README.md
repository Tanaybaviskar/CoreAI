# CoreAI - Agentic Workflow

A multi-agent AI system built with CrewAI and Google's Gemini LLM for automated content generation.

## 🚀 Features

- **Multi-Agent Workflow**: Researcher and Writer agents working collaboratively
- **AI-Powered Research**: Automated fact-finding and content research
- **Content Generation**: Professional article writing based on research findings
- **Gemini Integration**: Powered by Google's latest Gemini-1.5-flash model

## 📋 Prerequisites

- Python 3.8 or higher
- Google AI API key (from Google AI Studio)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tanaybaviskar/CoreAI.git
   cd CoreAI/backend/agentic
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the `backend/agentic` directory
   - Add your Google AI API key:
   ```env
   GOOGLE_API_KEY=your_google_ai_api_key_here
   ```

## 🔑 Getting Your Google AI API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and add it to your `.env` file

## 🏃‍♂️ Usage

Run the multi-agent workflow:

```bash
python main.py
```

The system will:
1. **Research Phase**: AI Researcher agent finds fascinating space facts
2. **Writing Phase**: Science Writer agent creates a structured article
3. **Output**: Generated content is displayed in the terminal

## 🤖 Agents

### AI Researcher
- **Role**: Finds interesting facts about space
- **Goal**: Research and compile fascinating space-related information
- **Backstory**: Expert in astronomy and astrophysics

### Science Writer
- **Role**: Creates engaging articles
- **Goal**: Transform research into readable content
- **Backstory**: Skilled science communicator

## 📁 Project Structure

```
backend/agentic/
├── main.py              # Main workflow script
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
└── README.md           # This file
```

## ⚙️ Configuration

You can customize the workflow by modifying:

- **Temperature**: Adjust creativity in `main.py` (line 10)
- **Model**: Change Gemini model version if needed
- **Agent Roles**: Modify agent backstories and goals
- **Tasks**: Update task descriptions and expected outputs

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **API Key Issues**
   - Verify your `.env` file exists and contains the correct API key
   - Ensure your Google AI API key is valid and has proper permissions

3. **Model Not Found**
   - The script uses `gemini-1.5-flash`. If unavailable, try `gemini-1.5-pro`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Links

- [CrewAI Documentation](https://docs.crewai.com/)
- [Google AI Studio](https://makersuite.google.com/)
- [LangChain Documentation](https://python.langchain.com/)
