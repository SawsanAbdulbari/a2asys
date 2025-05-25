import random
import os
import logging
from typing import Dict, List, Optional
from pathlib import Path

from google.adk.agents import Agent
from dotenv import load_dotenv
import praw
from praw.exceptions import PRAWException

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

class RedditScoutConfig:
    """Configuration for Reddit Scout agent."""
    DEFAULT_SUBREDDITS = {
        "gamedev": "General game development news",
        "unity3d": "Unity-specific news",
        "unrealengine": "Unreal Engine news"
    }
    DEFAULT_LIMIT = 5
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

def validate_reddit_credentials() -> bool:
    """Validate that all required Reddit API credentials are present."""
    required_vars = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        logger.error(f"Missing Reddit API credentials: {', '.join(missing)}")
        return False
    return True

def get_reddit_gamedev_news(subreddit: str, limit: int = RedditScoutConfig.DEFAULT_LIMIT) -> Dict[str, List[str]]:
    """
    Fetches top post titles from a specified subreddit using the Reddit API.

    Args:
        subreddit: The name of the subreddit to fetch news from (e.g., 'gamedev').
        limit: The maximum number of top posts to fetch.

    Returns:
        A dictionary with the subreddit name as key and a list of
        post titles as value. Returns an error message if credentials are
        missing, the subreddit is invalid, or an API error occurs.
    """
    logger.info(f"Fetching from r/{subreddit} via Reddit API")
    
    if not validate_reddit_credentials():
        return {subreddit: ["Error: Reddit API credentials not configured."]}

    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT"),
            timeout=10  # Add timeout to prevent hanging
        )
        
        # Check if subreddit exists and is accessible
        reddit.subreddits.search_by_name(subreddit, exact=True)
        sub = reddit.subreddit(subreddit)
        
        # Fetch hot posts with error handling
        try:
            top_posts = list(sub.hot(limit=limit))
        except Exception as e:
            logger.error(f"Error fetching posts from r/{subreddit}: {e}")
            return {subreddit: [f"Error fetching posts from r/{subreddit}. Please try again later."]}
        
        titles = [post.title for post in top_posts]
        if not titles:
            logger.warning(f"No recent hot posts found in r/{subreddit}")
            return {subreddit: [f"No recent hot posts found in r/{subreddit}."]}
            
        logger.info(f"Successfully fetched {len(titles)} posts from r/{subreddit}")
        return {subreddit: titles}
        
    except PRAWException as e:
        logger.error(f"Reddit API error for r/{subreddit}: {e}")
        return {subreddit: [f"Error accessing r/{subreddit}. It might be private, banned, or non-existent. Details: {e}"]}
    except Exception as e:
        logger.error(f"Unexpected error for r/{subreddit}: {e}")
        return {subreddit: [f"An unexpected error occurred while fetching from r/{subreddit}."]}

def get_mock_reddit_gamedev_news(subreddit: str) -> Dict[str, List[str]]:
    """
    Simulates fetching top post titles from a game development subreddit.
    Used for testing and development when Reddit API is unavailable.

    Args:
        subreddit: The name of the subreddit to fetch news from (e.g., 'gamedev').

    Returns:
        A dictionary with the subreddit name as key and a list of
        mock post titles as value. Returns a message if the subreddit is unknown.
    """
    logger.info(f"Simulating fetch from r/{subreddit}")
    
    mock_titles: Dict[str, List[str]] = {
        "gamedev": [
            "Show HN: My new procedural level generator using Rust",
            "Unity releases update 2023.3 LTS - Key features discussion",
            "Best practices for optimizing physics in networked multiplayer games",
            "Debate: Is ECS the future for all game engines? Performance comparison.",
            "Looking for constructive feedback on my indie game's pixel art style",
            "How to get started with Godot 4.2 GDScript",
            "Unreal Engine 5.4 Nanite & Lumen deep dive",
        ],
        "unrealengine": [
            "Unreal Engine 5.4 Performance Guide for large open worlds",
            "How to implement advanced Niagara particle effects for magic spells",
            "MetaHumans Animator tutorial: Lip sync and facial expressions",
            "Showcase: Sci-Fi cinematic created entirely in UE5",
            "Troubleshooting Lumen global illumination artifacts in indoor scenes",
            "Marketplace highlight: Advanced locomotion system",
            "Tips for migrating projects from UE4 to UE5",
        ],
        "unity3d": [
            "Best practices for mobile game optimization in Unity 2023 LTS",
            "Understanding Unity's Data-Oriented Technology Stack (DOTS) and Burst Compiler",
            "Tutorial: Creating custom PBR shaders with Unity Shader Graph",
            "Top free assets from the Unity Asset Store this month",
            "Migrating project from URP to HDRP - Common pitfalls and solutions",
            "Introduction to Unity Muse for texture generation",
            "Networking in Unity: Netcode for GameObjects vs Photon PUN",
        ]
    }
    
    normalized_subreddit = subreddit.lower()
    if normalized_subreddit in mock_titles:
        available_titles = mock_titles[normalized_subreddit]
        num_to_return = min(len(available_titles), 3)
        selected_titles = random.sample(available_titles, num_to_return)
        logger.info(f"Returning {num_to_return} mock titles for r/{subreddit}")
        return {subreddit: selected_titles}
    else:
        logger.warning(f"Unknown subreddit '{subreddit}' requested")
        return {subreddit: [f"Sorry, I don't have mock data for r/{subreddit}."]}

# Define the Agent
agent = Agent(
    name="reddit_scout_agent",
    description="A Reddit scout agent that searches for the most relevant posts in a given subreddit",
    model="gemini-1.5-flash-latest",
    instruction=(
        "You are the Game Dev News Scout. Your primary task is to fetch and summarize game development news.\n\n"
        "1. **Identify Intent:** Determine if the user is asking for game development news or related topics.\n"
        "2. **Determine Subreddit:** Identify which subreddit(s) to check:\n"
        "   - For general game dev news: use 'gamedev'\n"
        "   - For Unity-specific news: use 'unity3d'\n"
        "   - For Unreal Engine news: use 'unrealengine'\n"
        "   - If multiple topics are mentioned, check all relevant subreddits\n"
        "3. **Synthesize Output:** Take the exact list of titles returned by the tool.\n"
        "4. **Format Response:** Present the information as a concise, bulleted list. Clearly state which subreddit(s) the information came from.\n"
        "5. **MUST CALL TOOL:** You **MUST** call the `get_reddit_gamedev_news` tool with the identified subreddit(s). Do NOT generate summaries without calling the tool first.\n\n"
        "Example queries and responses:\n"
        "- 'What's new in game development?' -> Check r/gamedev\n"
        "- 'Show me Unity news' -> Check r/unity3d\n"
        "- 'Latest Unreal Engine updates' -> Check r/unrealengine\n"
        "- 'What's happening in game dev?' -> Check all three subreddits"
    ),
    tools=[get_reddit_gamedev_news],
    sub_agents=[]  # This agent doesn't have any sub-agents
)