"""
ElevenLabs Audio Agent - Professional Streamlit Interface
Real text-to-speech functionality with audio playback and voice selection.
"""

import streamlit as st
import sys
import os
import requests
import json
from datetime import datetime
import tempfile
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our ElevenLabs agent
try:
    from agents.audio.agent import (
        text_to_speech_elevenlabs, 
        validate_elevenlabs_api, 
        get_available_voices,
        ElevenLabsConfig
    )
    IMPORT_SUCCESS = True
except ImportError as e:
    IMPORT_SUCCESS = False
    IMPORT_ERROR = str(e)

def main():
    """Main ElevenLabs audio app."""
    st.set_page_config(
        page_title="ElevenLabs Audio Agent",
        page_icon="🎵",
        layout="wide"
    )
    
    # Header
    st.title("🎵 ElevenLabs Audio Agent")
    st.markdown("*Professional text-to-speech powered by ElevenLabs*")
    
    # Check imports
    if not IMPORT_SUCCESS:
        st.error(f"❌ Import Error: {IMPORT_ERROR}")
        st.info("Make sure you're running this from the correct directory and have ElevenLabs integration set up.")
        return
    
    # Sidebar configuration
    st.sidebar.header("🔧 Audio Configuration")
    
    # API Status Check
    st.sidebar.subheader("📡 API Status")
    if st.sidebar.button("🔄 Test API Connection"):
        with st.spinner("Testing ElevenLabs API..."):
            api_valid = validate_elevenlabs_api()
            if api_valid:
                st.sidebar.success("✅ API Connected")
            else:
                st.sidebar.error("❌ API Connection Failed")
                st.sidebar.info("Check your ELEVENLABS_API_KEY in .env file")
    
    # Voice Selection
    st.sidebar.subheader("🎤 Voice Selection")
    available_voices = list(ElevenLabsConfig.VOICES.keys())
    selected_voice = st.sidebar.selectbox(
        "Choose Voice:",
        available_voices,
        index=0,  # Rachel as default
        help="Select the voice for text-to-speech conversion"
    )
    
    # Voice preview info
    if selected_voice:
        st.sidebar.info(f"**Selected Voice:** {selected_voice}")
        st.sidebar.caption(f"Voice ID: {ElevenLabsConfig.VOICES[selected_voice]}")
    
    # Audio Settings
    st.sidebar.subheader("⚙️ Audio Settings")
    output_dir = st.sidebar.text_input(
        "Output Directory:",
        value=os.path.join(tempfile.gettempdir(), "a2a_audio"),
        help="Directory where audio files will be saved"
    )
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    st.sidebar.success(f"📁 Output: {output_dir}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Text-to-Speech Conversion")
        
        # Text input
        text_input = st.text_area(
            "Enter text to convert to speech:",
            height=150,
            placeholder="Enter your text here... (e.g., 'Welcome to our game development news update!')",
            help="Enter the text you want to convert to speech"
        )
        
        # Character count
        if text_input:
            char_count = len(text_input)
            st.caption(f"Characters: {char_count}")
            
            if char_count > 5000:
                st.warning("⚠️ Text is quite long. Consider breaking it into smaller chunks for better performance.")
        
        # Convert button
        col_a, col_b = st.columns([1, 3])
        
        with col_a:
            convert_button = st.button("🎵 Generate Speech", type="primary", disabled=not text_input)
        
        with col_b:
            if text_input:
                st.info(f"Will use voice: **{selected_voice}**")
        
        # Processing and results
        if convert_button and text_input:
            with st.spinner(f"🎵 Generating speech with {selected_voice} voice..."):
                try:
                    # Generate speech
                    result = text_to_speech_elevenlabs(
                        text=text_input,
                        voice_name=selected_voice,
                        output_dir=output_dir
                    )
                    
                    if result["success"]:
                        st.success("✅ Audio generated successfully!")
                        
                        # Display results
                        with st.expander("📊 Generation Details", expanded=True):
                            col_x, col_y, col_z = st.columns(3)
                            
                            with col_x:
                                st.metric("Voice Used", result["voice_name"])
                                st.metric("Text Length", f"{result['text_length']} chars")
                            
                            with col_y:
                                st.metric("File Size", f"{result['file_size']} bytes")
                                st.metric("Model", result["model"])
                            
                            with col_z:
                                file_path = result["file_path"]
                                st.metric("File Location", "✅ Saved")
                                st.code(file_path, language=None)
                        
                        # Audio player
                        if os.path.exists(result["file_path"]):
                            st.subheader("🔊 Audio Player")
                            
                            # Read audio file
                            with open(result["file_path"], "rb") as audio_file:
                                audio_bytes = audio_file.read()
                            
                            # Play audio
                            st.audio(audio_bytes, format="audio/mp3")
                            
                            # Download button
                            filename = os.path.basename(result["file_path"])
                            st.download_button(
                                label="📥 Download Audio File",
                                data=audio_bytes,
                                file_name=filename,
                                mime="audio/mp3"
                            )
                            
                            # Store in session state
                            st.session_state['last_audio'] = {
                                'file_path': result["file_path"],
                                'voice': result["voice_name"],
                                'text': text_input[:100] + "..." if len(text_input) > 100 else text_input,
                                'timestamp': datetime.now()
                            }
                        else:
                            st.error("❌ Audio file was generated but not found on disk")
                    else:
                        st.error(f"❌ Audio generation failed: {result['error']}")
                        
                        # Troubleshooting help
                        with st.expander("🔧 Troubleshooting"):
                            st.write("**Common solutions:**")
                            st.write("• Check your ElevenLabs API key in .env file")
                            st.write("• Verify internet connectivity")
                            st.write("• Ensure you have sufficient API credits")
                            st.write("• Try a shorter text sample")
                            
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
    
    with col2:
        st.header("📊 Audio Dashboard")
        
        # API Status
        st.subheader("🔗 API Status")
        try:
            api_valid = validate_elevenlabs_api()
            if api_valid:
                st.success("✅ ElevenLabs: Connected")
            else:
                st.error("❌ ElevenLabs: Disconnected")
        except:
            st.error("❌ ElevenLabs: Error")
        
        # Available Voices
        st.subheader("🎤 Available Voices")
        try:
            voices_result = get_available_voices()
            if voices_result["success"]:
                real_voices = voices_result["voices"]
                st.success(f"✅ {len(real_voices)} voices available")
                
                # Show first few voices
                for voice in real_voices[:5]:
                    voice_name = voice.get("name", "Unknown")
                    voice_category = voice.get("category", "")
                    st.caption(f"• {voice_name} ({voice_category})")
                
                if len(real_voices) > 5:
                    st.caption(f"... and {len(real_voices) - 5} more")
            else:
                st.warning("⚠️ Using local voice list")
                for voice in available_voices:
                    st.caption(f"• {voice}")
        except:
            st.warning("⚠️ Voice list unavailable")
        
        # Recent Activity
        if 'last_audio' in st.session_state:
            st.subheader("📈 Last Generation")
            last = st.session_state['last_audio']
            st.info(f"**Voice:** {last['voice']}")
            st.info(f"**Text:** {last['text']}")
            st.info(f"**Time:** {last['timestamp'].strftime('%H:%M:%S')}")
            
            # Quick actions
            if st.button("🔄 Regenerate"):
                st.info("Click 'Generate Speech' above to regenerate")
        
        # Usage Tips
        st.subheader("💡 Usage Tips")
        st.write("""
        **For best results:**
        • Use clear, well-punctuated text
        • Avoid special characters
        • Keep sentences reasonable length
        • Test with short samples first
        
        **Voice Selection:**
        • Rachel: Clear, professional
        • Domi: Warm, conversational  
        • Antoni: Deep, authoritative
        • Josh: Friendly, casual
        """)
    
    # Footer with technical info
    st.markdown("---")
    
    # Technical details
    with st.expander("🔧 Technical Details"):
        st.subheader("System Information")
        st.write(f"**ElevenLabs API Base URL:** {ElevenLabsConfig.BASE_URL}")
        st.write(f"**Default Model:** {ElevenLabsConfig.DEFAULT_MODEL}")
        st.write(f"**Output Directory:** {output_dir}")
        
        # Current settings
        st.subheader("Current Settings")
        st.json({
            "selected_voice": selected_voice,
            "voice_id": ElevenLabsConfig.VOICES.get(selected_voice, "unknown"),
            "output_directory": output_dir,
            "api_key_present": bool(os.getenv("ELEVENLABS_API_KEY"))
        })
    
    st.markdown("**🎵 ElevenLabs Audio Agent** | Professional TTS Integration | Status: Production Ready")

if __name__ == "__main__":
    main()