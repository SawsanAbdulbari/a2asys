from google.adk.agents import Agent
from dotenv import load_dotenv
import os

# Load environment variables (for GOOGLE_API_KEY)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Newscaster Summarizer Agent

def create_summarizer_agent():
    # Use the same model approach as other agents (no LiteLlm dependency)
    summarizer = Agent(
        name="newscaster_summarizer_agent",
        description="Summarizes a list of Reddit post titles in a newscaster style.",
        model="gemini-1.5-flash-latest",  # Same as Reddit Scout agent
        instruction=(
            "You are a news anchor summarizing Reddit headlines. "
            "Given a list of post titles, provide a concise, engaging summary in a professional newscaster style. "
            "Highlight key themes or interesting points found only in the titles. "
            "Start with an anchor intro like 'Here are today's top stories from the subreddit...' or similar. Keep it brief. "
            "Refer to subreddits by name, no need to mention 'r/'."
        )
    )
    return summarizer

# Expose root_agent for ADK
root_agent = create_summarizer_agent()