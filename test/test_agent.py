#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import praw
        print("✓ praw imported successfully")
        
        from google.adk.agents import Agent
        print("✓ google.adk.agents imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_env_vars():
    """Test if environment variables are loaded"""
    required_vars = ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            print(f"✓ {var} is set")
    
    if missing_vars:
        print(f"✗ Missing environment variables: {missing_vars}")
        return False
    
    return True

def test_agent_import():
    """Test if the agent can be imported"""
    try:
        from agents.reddit_scout.agent import agent
        print(f"✓ Agent imported successfully: {agent.name}")
        return True
    except Exception as e:
        print(f"✗ Agent import error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Reddit Scout Agent Setup...\n")
    
    print("1. Testing package imports:")
    imports_ok = test_imports()
    
    print("\n2. Testing environment variables:")
    env_ok = test_env_vars()
    
    print("\n3. Testing agent import:")
    agent_ok = test_agent_import()
    
    print("\n" + "="*50)
    if imports_ok and env_ok and agent_ok:
        print("🎉 All tests passed! Setup is complete.")
    else:
        print("❌ Some tests failed. Please check the setup.")
        sys.exit(1)
