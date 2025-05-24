# Reddit Scout Agent

A Reddit scout agent that searches for the most relevant posts in game development subreddits using Google's ADK (Agent Development Kit).

## Features

- Fetches top posts from specified subreddits using Reddit API
- Supports multiple game development subreddits (gamedev, unrealengine, unity3d)
- Includes mock data fallback for testing
- Built with Google ADK agents framework

## Prerequisites

- Python 3.8 or higher
- WSL (Windows Subsystem for Linux)
- Reddit API credentials

## Setup Instructions

### 1. Clone and Navigate
```bash
cd /path/to/a2asys
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Reddit API Setup

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - Name: Your app name
   - App type: Select "script"
   - Description: Optional
   - About URL: Leave blank
   - Redirect URI: http://localhost:8080
4. Click "Create app"
5. Note down your `client_id` (under the app name) and `client_secret`

### 5. Environment Configuration

Create a `.env` file in the project root:
```bash
touch .env
```

Add your Reddit API credentials to `.env`:
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=YourAppName/1.0 by YourUsername
```

**Important**: Replace the placeholder values with your actual Reddit API credentials.

### 6. Google ADK Setup

Install Google ADK if not already installed:
```bash
pip install google-adk
```

You may need to authenticate with Google Cloud if required by the ADK.

## Usage

### Running the Agent

```python
from agents.reddit_scout.agent import agent

# The agent is configured to work with these subreddits:
# - gamedev (default)
# - unrealengine  
# - unity3d

# Example usage would depend on how you integrate with Google ADK
```

### Supported Subreddits

- **gamedev**: General game development discussions
- **unrealengine**: Unreal Engine specific content
- **unity3d**: Unity game engine content

## Project Structure

```
a2asys/
├── agents/
│   └── reddit_scout/
│       └── agent.py          # Main agent implementation
├── .env                      # Environment variables (create this)
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Functions

### `get_reddit_gamedev_news(subreddit, limit=5)`
- Fetches real data from Reddit API
- Returns dictionary with subreddit name and list of post titles
- Handles errors gracefully

### `get_mock_reddit_gamedev_news(subreddit)`
- Provides mock data for testing
- Useful when API credentials are not available
- Returns sample game development posts

## Error Handling

The agent includes comprehensive error handling for:
- Missing API credentials
- Invalid or private subreddits
- Network connectivity issues
- API rate limiting

## Development

### Testing Without API
To test without Reddit API credentials, modify the agent to use the mock function:
```python
# In agent.py, change the tools list to:
tools=[get_mock_reddit_gamedev_news],
```

### Adding New Subreddits
To support additional subreddits, add mock data to the `mock_titles` dictionary in `get_mock_reddit_gamedev_news()`.

## Troubleshooting

### Common Issues

1. **"Reddit API credentials missing"**
   - Ensure `.env` file exists and contains valid credentials
   - Check that variable names match exactly

2. **"Module not found" errors**
   - Activate virtual environment: `source venv/bin/activate`
   - Install requirements: `pip install -r requirements.txt`

3. **Google ADK authentication issues**
   - Follow Google ADK documentation for authentication
   - Ensure proper Google Cloud project setup

### WSL Specific Notes

- Use `python3` instead of `python` if needed
- Ensure proper line endings (LF, not CRLF)
- Virtual environment activation: `source venv/bin/activate`

## Security

- Never commit your `.env` file to version control
- Keep your Reddit API credentials secure
- Consider using environment variables in production

## VS Code Setup for WSL

### 1. Open Project in VS Code with WSL
```bash
# From WSL terminal, navigate to project directory
cd /mnt/d/ai/saas/a2asys

# Open in VS Code
code .
```

### 2. Install Required VS Code Extensions

**Essential Extensions:**
- **WSL** (ms-vscode-remote.vscode-remote-extensionpack)
- **Python** (ms-python.python)
- **Python Debugger** (ms-python.debugpy)
- **Pylance** (ms-python.vscode-pylance)

**Install via Command Palette:**
1. Press `Ctrl+Shift+P`
2. Type "Extensions: Install Extension"
3. Search and install each extension

### 3. Configure Python Environment in VS Code

**Step 1: Create Virtual Environment**
```bash
# In VS Code integrated terminal (Ctrl+`)
# Ensure you're in WSL (should show user@hostname)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your prompt should now show (venv)
```

**Step 2: Select Python Interpreter**
1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `./venv/bin/python` (should show Python version)
4. VS Code status bar should now show the selected interpreter

**Step 3: Install Dependencies**
```bash
# Ensure virtual environment is activated (venv should be in prompt)
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create and Configure Environment File

**Create .env file:**
```bash
# In VS Code terminal
touch .env
```

**Add to .env file (use VS Code editor):**
```env
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=YourAppName/1.0 by YourUsername
```

### 5. VS Code Workspace Configuration

**Create .vscode/settings.json:**
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### 6. Testing the Setup

**Create a test file: `test_agent.py`**
```python
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
```

**Run the test:**
```bash
# In VS Code terminal with activated venv
python test_agent.py
```

### 7. Debugging Configuration

**Create .vscode/launch.json for debugging:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env",
            "python": "${workspaceFolder}/venv/bin/python"
        },
        {
            "name": "Test Reddit Agent",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/test_agent.py",
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env",
            "python": "${workspaceFolder}/venv/bin/python"
        }
    ]
}
```

### 8. Quick Commands

**Useful VS Code shortcuts:**
- `Ctrl+`` - Toggle integrated terminal
- `Ctrl+Shift+P` - Command palette
- `F5` - Start debugging
- `Ctrl+F5` - Run without debugging
- `Ctrl+Shift+X` - Extensions panel

**Terminal commands:**
```bash
# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install new package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt

# Run Python file
python filename.py
```

## License

This project is for educational/development purposes. Ensure compliance with Reddit's API terms of service when using in production.
