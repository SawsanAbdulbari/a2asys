"""
ElevenLabs Audio Agent - Production Version
Professional text-to-speech using ElevenLabs API.
"""

import os
import tempfile
import requests
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from google.adk.agents import Agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Configure logging
logger = logging.getLogger(__name__)

class ElevenLabsConfig:
    """Configuration for ElevenLabs TTS."""
    API_KEY = os.getenv("ELEVENLABS_API_KEY")
    BASE_URL = "https://api.elevenlabs.io/v1"
    DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
    DEFAULT_MODEL = "eleven_monolingual_v1"
    
    # Voice options
    VOICES = {
        "Rachel": "21m00Tcm4TlvDq8ikWAM",
        "Domi": "AZnzlk1XvdvUeBnXmlld", 
        "Bella": "EXAVITQu4vr4xnSDxMaL",
        "Antoni": "ErXwobaYiN019PkySvjV",
        "Elli": "MF3mGyEYCl7XYWbV9V6O",
        "Josh": "TxGEqnHWrfWFTfGW9XjX",
        "Arnold": "VR6AewLTigWG4xSOukaG",
        "Adam": "pNInz6obpgDQGcFmaJgB",
        "Sam": "yoZ06aMxZJJ28mfd3POQ"
    }

def validate_elevenlabs_api() -> bool:
    """Validate ElevenLabs API key and connectivity."""
    if not ElevenLabsConfig.API_KEY:
        logger.error("ElevenLabs API key not found in environment variables")
        return False
    
    try:
        # Test API connectivity
        headers = {"xi-api-key": ElevenLabsConfig.API_KEY}
        response = requests.get(f"{ElevenLabsConfig.BASE_URL}/voices", headers=headers, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ ElevenLabs API validation successful")
            return True
        else:
            logger.error(f"❌ ElevenLabs API validation failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ ElevenLabs API validation error: {e}")
        return False

def text_to_speech_elevenlabs(
    text: str, 
    voice_name: str = "Rachel", 
    model: str = None,
    output_dir: str = None
) -> Dict[str, Any]:
    """Convert text to speech using ElevenLabs API."""
    try:
        # Validate API
        if not validate_elevenlabs_api():
            return {
                "success": False,
                "error": "ElevenLabs API validation failed. Check your API key.",
                "file_path": None
            }
        
        # Get voice ID
        voice_id = ElevenLabsConfig.VOICES.get(voice_name, ElevenLabsConfig.DEFAULT_VOICE_ID)
        if not model:
            model = ElevenLabsConfig.DEFAULT_MODEL
            
        # Prepare request
        url = f"{ElevenLabsConfig.BASE_URL}/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ElevenLabsConfig.API_KEY
        }
        
        # Request payload
        data = {
            "text": text,
            "model_id": model,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        logger.info(f"🔊 Generating speech for text: {text[:50]}...")
        logger.info(f"🎤 Using voice: {voice_name} ({voice_id})")
        
        # Make API request
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Create output directory
            if not output_dir:
                output_dir = os.path.join(tempfile.gettempdir(), "a2a_audio")
            
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate unique filename
            import time
            timestamp = int(time.time())
            filename = f"tts_{timestamp}_{voice_name.lower()}.mp3"
            file_path = os.path.join(output_dir, filename)
            
            # Save audio file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            logger.info(f"✅ Audio generated successfully: {file_path}")
            logger.info(f"📊 File size: {file_size} bytes")
            
            return {
                "success": True,
                "file_path": file_path,
                "voice_name": voice_name,
                "voice_id": voice_id,
                "model": model,
                "text_length": len(text),
                "file_size": file_size,
                "error": None
            }
        else:
            error_msg = f"ElevenLabs API error: {response.status_code} - {response.text}"
            logger.error(f"❌ {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "file_path": None
            }
            
    except Exception as e:
        error_msg = f"Text-to-speech conversion failed: {str(e)}"
        logger.error(f"❌ {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "file_path": None
        }

def get_available_voices() -> Dict[str, Any]:
    """Get list of available ElevenLabs voices."""
    try:
        if not validate_elevenlabs_api():
            return {"success": False, "voices": [], "error": "API validation failed"}
            
        headers = {"xi-api-key": ElevenLabsConfig.API_KEY}
        response = requests.get(f"{ElevenLabsConfig.BASE_URL}/voices", headers=headers, timeout=10)
        
        if response.status_code == 200:
            voices_data = response.json()
            return {
                "success": True,
                "voices": voices_data.get("voices", []),
                "error": None
            }
        else:
            return {
                "success": False,
                "voices": [],
                "error": f"API error: {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "voices": [],
            "error": str(e)
        }

# Enhanced TTS function for ADK Agent
def elevenlabs_tts_tool(text: str, voice_name: str = "Rachel") -> str:
    """TTS tool function for ADK Agent."""
    result = text_to_speech_elevenlabs(text, voice_name)
    
    if result["success"]:
        return f"Audio file generated successfully. File saved as: {result['file_path']}. Voice used: {result['voice_name']}. File size: {result['file_size']} bytes."
    else:
        return f"Audio generation failed: {result['error']}"

# Create the Real ElevenLabs Audio Agent
def create_elevenlabs_agent():
    """Create the real ElevenLabs audio agent."""
    
    agent_instance = Agent(
        name="elevenlabs_audio_agent",
        description="Professional text-to-speech agent using ElevenLabs API",
        model="gemini-1.5-flash-latest",
        instruction=(
            "You are a professional Text-to-Speech agent powered by ElevenLabs. "
            "You convert text to high-quality speech audio files. "
            
            "IMPORTANT RESPONSE FORMAT:\n"
            "When text-to-speech is successful, respond with:\n"
            "'I've converted your text to speech. The audio file is saved at `[FULL_FILE_PATH]`'\n"
            
            "Available voices: Rachel (default), Domi, Bella, Antoni, Elli, Josh, Arnold, Adam, Sam\n"
            "Always use voice_name='Rachel' unless specifically requested otherwise.\n"
            
            "For errors, explain what went wrong and suggest solutions.\n"
            "Keep responses professional and helpful."
        ),
        tools=[elevenlabs_tts_tool],
    )
    
    return agent_instance

# Export the agent
root_agent = create_elevenlabs_agent()