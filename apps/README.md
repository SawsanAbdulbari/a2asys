# A2A System - Web Applications

This directory contains Streamlit web applications for interacting with your A2A agents.

## 🚀 Quick Start

1. **Install Streamlit** (if not already installed):
   ```bash
   pip install streamlit
   ```

2. **Run any app** from the project root:
   ```bash
   # Reddit Scout Web Interface
   streamlit run apps/reddit_scout_app.py
   
   # Complete Pipeline Demo
   streamlit run apps/pipeline_demo_app.py
   ```

## 📱 Available Applications

### 1. Reddit Scout App (`reddit_scout_app.py`)
**Purpose:** Web interface for fetching game development news from Reddit.

**Features:**
- ✅ Select from multiple subreddits (gamedev, unity3d, unrealengine, etc.)
- ✅ Configure number of posts to fetch
- ✅ Switch between real API and mock data
- ✅ Real-time API status monitoring
- ✅ Copy functionality for posts

**URL:** http://localhost:8501

### 2. Pipeline Demo App (`pipeline_demo_app.py`)
**Purpose:** Complete workflow demonstration: Reddit → Summarizer → Audio.

**Features:**
- ✅ Full pipeline execution
- ✅ Step-by-step progress tracking
- ✅ Visual workflow representation
- ✅ Results summary and statistics
- ✅ Technical details and system status

**URL:** http://localhost:8501

## 🔧 Usage Instructions

### Reddit Scout App
1. Start the app: `streamlit run apps/reddit_scout_app.py`
2. Select your preferred subreddit from the sidebar
3. Configure the number of posts (1-10)
4. Choose real API or mock data
5. Click "Fetch Latest Posts"
6. View and copy the results

### Pipeline Demo App  
1. Start the app: `streamlit run apps/pipeline_demo_app.py`
2. Select subreddit and number of posts
3. Click "Run Complete Pipeline"
4. Watch the progress through all 3 steps:
   - Reddit data fetching
   - News summarization
   - Audio generation (mock)
5. Review the complete results

## 🎯 Advanced Features

### Session State
Both apps use Streamlit session state to:
- Remember last fetched data
- Track API usage
- Maintain user preferences

### Error Handling
- Graceful handling of API failures
- Fallback to mock data when needed
- Clear error messages and troubleshooting tips

### Real-time Status
- API connectivity monitoring
- Agent health checks
- Processing time tracking

## 🚀 Next Steps

### Ready for Production:
- ✅ Reddit API integration working
- ✅ Web interface fully functional
- ✅ Error handling and fallbacks
- ✅ Professional UI design

### Future Enhancements:
- [ ] Real ElevenLabs TTS integration
- [ ] User authentication and sessions
- [ ] Data export functionality
- [ ] Advanced filtering and search
- [ ] Custom subreddit management
- [ ] Audio player integration

## 🔗 Integration

These apps work seamlessly with your existing A2A agents:
- **Reddit Scout Agent** - Fetches real Reddit data
- **Summarizer Agent** - Generates professional summaries
- **Audio Agent** - Creates speech output (mock ready for real TTS)

## 🛠️ Troubleshooting

### Common Issues:

1. **Import Errors:**
   - Ensure you're running from the project root directory
   - Check that all agents are properly set up

2. **API Errors:**
   - Verify `.env` file has correct Reddit credentials
   - Check internet connectivity
   - Try switching to mock data

3. **Port Conflicts:**
   - Streamlit uses port 8501 by default
   - Use `streamlit run app.py --server.port 8502` for different port

### Getting Help:
- Check the main project README
- Run the test scripts: `python scripts/test_all.ps1`
- Verify agent status: `python agents/test_final_working.py`

---

**🎮 A2A Web Apps** | Professional interfaces for your multi-agent system