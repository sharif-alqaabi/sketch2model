# 🏠 Sketch2Model - AI Multi-Agent House Design System

Transform hand-drawn sketches and voice descriptions into professional 3D architectural designs with AI-powered cost estimation. **Sketch2Model** uses a sophisticated multi-agent architecture powered by **Anthropic Claude**, **Fish Audio**, and **Fetch.ai** to bring your house designs to life.

## ✨ Key Features

### 🎨 **Drawing Input**
- Interactive canvas with customizable brushes and colors
- Touch support for tablets and mobile devices
- Real-time drawing with smooth rendering
- Download and save your sketches

### 🎤 **Voice Input**
- Record voice descriptions of your house design
- Automatic speech-to-text transcription (Fish Audio API)
- Generate 3D designs directly from voice
- No drawing skills required!

### 🤖 **AI-Powered 3D Generation**
- **Claude Sonnet 4 Vision** analyzes drawings and descriptions
- Identifies architectural style, structure, and features
- Estimates dimensions and proportions
- Generates photorealistic 3D renderings (Pollinations AI)
- Professional architectural visualization

### 💰 **Intelligent Cost Estimation**
- **AI-powered analysis** of house size and complexity
- **Dynamic pricing** based on actual square footage
- **Current market prices** (2024-2025 US market)
- **Itemized breakdown** by category:
  - Structural materials (concrete, bricks, steel)
  - Finishing materials (paint, tiles, doors)
  - Roofing materials (tiles, trusses, waterproofing)
  - Fixtures (windows, electrical, plumbing)
- **Labor cost calculation** (30-40% of materials)
- **Detailed notes** with methodology and assumptions

### 🎯 **Multi-Agent Architecture**
- **RootAgent**: Orchestrates the entire workflow
- **GeneratorAgent**: Creates 3D designs from drawings/voice
- **EstimatorAgent**: Calculates realistic construction costs
- **VoiceAgent**: Converts speech to text descriptions
- **BaseAgent**: Foundation for all agents with shared functionality

### 🎨 **Modern UI/UX**
- Clean, professional interface
- Responsive design (desktop, tablet, mobile)
- Smooth animations and transitions
- Real-time feedback and loading states
- Professional cost breakdown tables

## 🛠️ Tech Stack

### **Frontend**
- React 18 + Vite
- Modern CSS with animations
- Canvas API for drawing
- MediaRecorder API for voice input
- Responsive design

### **Backend**
- FastAPI (Python)
- Multi-agent architecture
- Async/await for performance
- RESTful API design

### **AI & APIs**

#### **🤖 Anthropic Claude Sonnet 4**
- **Used in**: GeneratorAgent, EstimatorAgent
- **Purpose**: 
  - Vision analysis of house drawings
  - Architectural design generation
  - AI-powered cost estimation with market prices
- **Cost**: ~$0.01-0.02 per request
- **Website**: [anthropic.com](https://www.anthropic.com/)

#### **🎤 Fish Audio**
- **Used in**: VoiceAgent
- **Purpose**: 
  - Speech-to-text transcription
  - Voice input processing
- **Cost**: Free tier available
- **Website**: [fish.audio](https://fish.audio/)

#### **🤝 Fetch.ai**
- **Used in**: Multi-Agent System Architecture
- **Agent**: `@material-estimation-agent-0`
- **Profile**: [View on Agentverse](https://agentverse.ai/agents/details/agent1qv0x7tjd4mhn7km9mmz7p839umzjstf4wp0vepzwfz8xymnaac2vs5he7l7/profile)
- **Purpose**: 
  - Agent orchestration and coordination
  - Inter-agent communication
  - Workflow management
- **Website**: [fetch.ai](https://fetch.ai/)

#### **🎨 Pollinations AI**
- **Used in**: GeneratorAgent (Image Generation)
- **Purpose**: Photorealistic 3D rendering (Flux model)
- **Cost**: Free
- **Website**: [pollinations.ai](https://pollinations.ai/)

### **Deployment**
- **Frontend**: Netlify (Free tier, auto-deploy)
- **Backend**: Render.com (Free or $7/month)
- **Total Cost**: $0-7/month + API usage

## 🤝 Technology Partners & Usage

This project leverages cutting-edge AI and multi-agent technologies from industry leaders:

### **1. Anthropic (Claude Sonnet 4)**
- **Agents**: GeneratorAgent, EstimatorAgent
- **Capabilities**:
  - Vision API for analyzing hand-drawn house sketches
  - Natural language processing for architectural descriptions
  - Intelligent cost estimation with market price analysis
- **API Calls**: 2-3 per complete workflow
- **Cost**: ~$0.01-0.02 per request

### **2. Fish Audio**
- **Agent**: VoiceAgent
- **Capabilities**:
  - High-quality speech-to-text transcription
  - Multi-language support
  - Real-time audio processing
- **API Calls**: 1 per voice input
- **Cost**: Free tier available

### **3. Fetch.ai**
- **Component**: Multi-Agent System Architecture
- **Agent Name**: `@material-estimation-agent-0`
- **Agent Profile**: [View on Agentverse](https://agentverse.ai/agents/details/agent1qv0x7tjd4mhn7km9mmz7p839umzjstf4wp0vepzwfz8xymnaac2vs5he7l7/profile)
- **Capabilities**:
  - Agent orchestration and coordination
  - Inter-agent communication protocols
  - Workflow management and execution
  - Context sharing between agents
- **Implementation**: RootAgent uses Fetch.ai patterns for agent coordination

### **4. Pollinations AI**
- **Agent**: GeneratorAgent (Image Generation)
- **Capabilities**:
  - Flux model for photorealistic rendering
  - High-quality 3D architectural visualization
  - Fast image generation
- **Cost**: Free

---

## 🏗️ Architecture

### Multi-Agent System

```
                    ┌─────────────────┐
                    │   RootAgent     │
                    │  (Orchestrator) │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │  Generator   │   │  Estimator   │   │    Voice     │
  │    Agent     │   │    Agent     │   │    Agent     │
  └──────────────┘   └──────────────┘   └──────────────┘
         │                   │                   │
         ├─ Claude Vision    ├─ Claude Vision    ├─ Fish Audio
         ├─ Design Analysis  ├─ Cost Analysis    ├─ Speech-to-Text
         └─ 3D Generation    └─ Market Pricing   └─ Design Gen
```

**See [AGENTS.md](AGENTS.md) for complete agent documentation.**

### Workflow

#### Drawing Mode:
```
User Drawing → GeneratorAgent → EstimatorAgent → Results
                    ↓                  ↓
              3D Rendering      Cost Breakdown
```

#### Voice Mode:
```
Voice Recording → VoiceAgent → GeneratorAgent → EstimatorAgent → Results
                      ↓              ↓                ↓
                Transcription   3D Rendering    Cost Breakdown
```

### File Structure

```
sketch2model/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── agents/
│   │   ├── base_agent.py       # Abstract base class
│   │   ├── root_agent.py       # Workflow orchestrator
│   │   ├── generator_agent.py  # 3D design generation
│   │   ├── estimator_agent.py  # AI cost estimation
│   │   └── voice_agent.py      # Speech-to-text
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Docker configuration
│   └── .env.example            # Environment template
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main application
│   │   ├── components/
│   │   │   ├── DrawingCanvas.jsx   # Drawing interface
│   │   │   ├── Toolbar.jsx         # Drawing tools
│   │   │   ├── VoiceInput.jsx      # Voice recorder
│   │   │   └── ResultPanel.jsx     # Results display
│   │   └── ...
│   ├── netlify.toml            # Netlify config
│   └── .env.production         # Production env vars
├── AGENTS.md                   # Agent documentation
├── DEPLOY.md                   # Deployment guide
├── AI_COST_ESTIMATION.md       # Cost estimation details
└── README.md                   # This file
```

## 📋 Prerequisites

### **Required:**
- Python 3.11+
- Node.js 18+
- npm or yarn

### **API Keys:**

#### **Anthropic API Key** (Required)
- **Get here**: [console.anthropic.com](https://console.anthropic.com/)
- **Used by**: GeneratorAgent, EstimatorAgent
- **Purpose**: Vision analysis, design generation, cost estimation
- **Cost**: ~$0.01-0.02 per request (~2-3 API calls per workflow)
  
#### **Fish Audio API Key** (Required for Voice Mode)
- **Get here**: [fish.audio](https://fish.audio/)
- **Used by**: VoiceAgent
- **Purpose**: Speech-to-text transcription
- **Cost**: Free tier available

## 🚀 Quick Start (Local Development)

### 1. Clone & Install

```bash
git clone <repository-url>
cd sketch2model

# Backend setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..
```

### 2. Configure Environment

```bash
cd backend
cp .env.example .env
# Edit .env and add:
# ANTHROPIC_API_KEY=your_anthropic_key_here
# FISH_AUDIO_API_KEY=your_fish_audio_key_here
```

### 3. Run Application

```bash
# From project root
./start.sh
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## 🌐 Deploy to Production

See **[DEPLOY.md](DEPLOY.md)** for complete deployment instructions.

**Quick Deploy (30 minutes):**
- Backend: Render.com (Free or $7/month)
- Frontend: Netlify (Free)
- Total Cost: $0-7/month

## 📖 Usage

### **Drawing Mode:**

1. **Draw Your House**
   - Use brush tool to sketch your house design
   - Choose colors from the palette
   - Adjust brush size as needed
   - Include windows, doors, roof details

2. **Generate 3D Design**
   - Click "Generate 3D Design" button
   - AI analyzes your drawing (3-8 seconds)
   - View photorealistic 3D rendering
   - Read architectural analysis

3. **Estimate Costs**
   - Click "Estimate Cost" button
   - AI analyzes house size and materials (5-12 seconds)
   - View itemized cost breakdown
   - See total cost with materials + labor

### **Voice Mode:**

1. **Record Voice Description**
   - Switch to "Voice Input" tab
   - Click microphone button
   - Describe your house design verbally
   - Stop recording when done

2. **Generate from Voice**
   - AI transcribes your voice (2-5 seconds)
   - Generates 3D design from description
   - View rendering and cost estimate

### **Example Voice Prompts:**
- "I want a two-story modern house with large windows and a flat roof"
- "Design a colonial style house with brick exterior and white trim"
- "Create a small cottage with a pitched roof and front porch"

## 💰 Cost Estimation Details

### **How It Works:**
1. AI analyzes the house image to estimate square footage
2. Calculates required materials based on size
3. Uses current 2024-2025 US market prices
4. Computes labor costs (30-40% of materials)

### **Market Prices Used:**
- Concrete: $150-200 per cubic yard
- Bricks: $0.50-0.80 per brick
- Paint: $30-50 per gallon
- Windows: $400-600 per unit
- Doors: $300-500 per unit
- [See AI_COST_ESTIMATION.md for complete list]

### **Typical Cost Ranges:**
- **Small House (800-1,200 sq ft):** $30,000 - $60,000
- **Medium House (1,500-2,000 sq ft):** $60,000 - $100,000
- **Large House (2,500-3,500 sq ft):** $100,000 - $180,000

*Note: Estimates are for materials + basic labor only. Does not include land, permits, or premium finishes.*

## 🎨 Drawing Tips

For best AI analysis results:
- Draw clear outlines of walls and structure
- Include windows, doors, and roof details
- Add perspective if possible
- Use different colors for different elements
- Make the drawing as detailed as possible

## 🐛 Troubleshooting

### **Backend Issues**

**Backend won't start:**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r backend/requirements.txt`
- Check API keys in `backend/.env`

**API errors:**
- Verify Anthropic API key is valid
- Check Fish Audio API key (for voice mode)
- Ensure backend is running on port 8000
- Check backend logs for detailed errors

### **Frontend Issues**

**Frontend won't start:**
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version` (requires 18+)
- Clear Vite cache: `rm -rf node_modules/.vite`

**CORS errors:**
- Check `ALLOWED_ORIGINS` in backend environment variables
- Verify frontend URL is added to backend CORS settings

### **Deployment Issues**

**Render deployment fails:**
- Check build logs in Render dashboard
- Verify all environment variables are set
- See [DEPLOY.md](DEPLOY.md) for troubleshooting

**Netlify deployment fails:**
- Check build logs in Netlify dashboard
- Verify `VITE_API_URL` environment variable is set
- Ensure no trailing slash in API URL

## 📚 Documentation

- **[AGENTS.md](AGENTS.md)** - Complete multi-agent system documentation
- **[DEPLOY.md](DEPLOY.md)** - Production deployment guide (Render + Netlify)
- **[AI_COST_ESTIMATION.md](AI_COST_ESTIMATION.md)** - Cost estimation system details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

See LICENSE file for details.

## 🙏 Acknowledgments

### **AI & Technology Partners:**
- **[Anthropic](https://www.anthropic.com/)** - Claude Sonnet 4 for vision analysis and intelligent cost estimation
- **[Fish Audio](https://fish.audio/)** - Speech-to-text API for voice input
- **[Fetch.ai](https://fetch.ai/)** - Multi-agent system architecture and orchestration
- **[Pollinations AI](https://pollinations.ai/)** - Photorealistic 3D image generation

### **Infrastructure:**
- **[Render](https://render.com/)** - Backend hosting
- **[Netlify](https://www.netlify.com/)** - Frontend hosting

### **Open Source:**
- React and FastAPI communities

---

## 🚀 Quick Links

- **Live Demo**: [Your deployed URL]
- **Documentation**: [AGENTS.md](AGENTS.md), [DEPLOY.md](DEPLOY.md)
- **API Docs**: Visit `/docs` on your backend URL
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)

---

## 📊 Sketch2Model Stats

- **Project Name**: Sketch2Model
- **Agents**: 4 specialized AI agents + 1 orchestrator
- **API Calls**: 2-3 per complete workflow
- **Average Response Time**: 10-20 seconds
- **Cost per Request**: ~$0.01-0.02
- **Supported Formats**: Drawing (PNG) + Voice (WebM/WAV/MP3)
- **Deployment**: Production-ready on Render + Netlify

---

**Sketch2Model - Built with ❤️ using AI Multi-Agent Architecture**