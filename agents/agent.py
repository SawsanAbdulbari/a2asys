from google.adk.agents import Agent
from agents.reddit_scout.agent import agent as reddit_scout_agent

# Define the root agent that will coordinate other agents
root_agent = Agent(
    name="root_agent",
    description="Root agent that coordinates other specialized agents",
    model="gemini-1.5-flash-latest",
    instruction=(
        "You are the root coordinator agent. Your role is to:\n"
        "1. Understand user requests and delegate to appropriate specialized agents\n"
        "2. Coordinate between different agents when needed\n"
        "3. Provide clear, helpful responses to users\n\n"
        "IMPORTANT: When a user asks about game development news, Reddit posts, or anything related to game development communities, "
        "you MUST transfer the request to the reddit_scout_agent using the transfer_to_agent function.\n\n"
        "Example transfers:\n"
        "- 'What's new in game development?' -> transfer to reddit_scout_agent\n"
        "- 'Show me Unity news' -> transfer to reddit_scout_agent\n"
        "- 'Latest Unreal Engine updates' -> transfer to reddit_scout_agent\n\n"
        "Only handle general questions yourself. All game development related queries should be transferred."
    ),
    tools=[],  # Root agent doesn't need direct tools
    sub_agents=[reddit_scout_agent]  # Use sub_agents instead of agents
) 