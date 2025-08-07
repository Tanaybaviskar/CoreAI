import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew

# Load API key
load_dotenv()

# Set up Gemini-Pro via LangChain
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

# Agents
researcher = Agent(
    role="AI Researcher",
    goal="Find interesting facts about space",
    backstory="Expert in astronomy and astrophysics, curious and detailed.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

writer = Agent(
    role="Science Writer",
    goal="Write a short article on the topic provided by the researcher",
    backstory="Skilled science communicator who turns complex ideas into readable content.",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

# Tasks
task1 = Task(
    description="Research and list 5 fascinating facts about space.",
    expected_output="A list of 5 fascinating facts about space with brief explanations.",
    agent=researcher,
)

task2 = Task(
    description="Write a short article based on the facts about space provided by the researcher.",
    expected_output="A well-written short article about space facts in 200-300 words.",
    agent=writer,
)

# Crew setup
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=True,
)

# Run workflow
if __name__ == "__main__":
    result = crew.kickoff()
    print("\n\nFinal Output:\n", result)
