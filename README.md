# Streamlit Prompt Runner

## Overview

The **Streamlit Prompt Runner** is a web application for urban planning compliance checking with 3D visualization. It allows users to input prompts, generate structured JSON specifications, check building compliance against DCR regulations, and visualize buildings in 3D.

---

## ✨ Features

- 🎨 **AI-Powered Design** - Natural language → JSON specifications
- ✅ **Compliance Checking** - Multi-city DCR regulation validation
- 🏗️ **3D Visualization** - Interactive GLB model viewer
- 👍👎 **RL Feedback System** - Reinforcement learning from user feedback
- 🌆 **Multi-City Support** - Mumbai, Ahmedabad, Pune, Nashik
- 📊 **Complete Logging** - Prompt and action tracking
- 🧪 **Tested** - 82 tests with 94% pass rate

---

## 🚀 Quick Start

### Installation

```bash
# 1. Clone repository
cd "C:\prompt runner\streamlit-prompt-runner"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start MongoDB (if not running)
mongod

# 4. Start MCP Server (Terminal 1)
python mcp_server.py

# 5. Start Streamlit App (Terminal 2)
streamlit run main.py

# 6. Open browser
http://localhost:8501
```

---

## 📋 Project Structure

```
streamlit-prompt-runner/
├── main.py                # Main Streamlit application
├── mcp_server.py          # MCP Flask API server
├── upload_rules.py        # Upload city rules to database
├── requirements.txt       # Python dependencies
│
├── agents/                # AI Agents
│   ├── design_agent.py    # Prompt → JSON spec
│   ├── calculator_agent.py # Compliance checking
│   ├── geometry_agent.py   # 3D generation
│   └── rl_agent.py         # Reinforcement learning
│
├── components/            # UI Components
│   ├── glb_viewer.py      # 3D GLB viewer
│   └── ui.py              # UI helpers
│
├── utils/                 # Utilities
│   ├── geometry_converter.py # JSON → GLB conversion
│   └── io_helpers.py          # File operations
│
├── tests/                 # Test Suite (82 tests)
│   ├── test_mcp.py
│   ├── test_agents.py
│   ├── test_geometry.py
│   └── conftest.py
│
├── mcp_data/              # Data Storage
│   └── rules.json         # 53 rules, 4 cities
│
└── outputs/geometry/      # Generated 3D models
```

---

## 🎯 Usage

### **1. Design Studio**
Enter a prompt:
```
"Design a 7-story residential building in Mumbai with setback 3m"
```
Get structured JSON specification.

### **2. Compliance Checker**
- Select city (Mumbai/Ahmedabad/Pune/Nashik)
- Enter building parameters
- Check compliance against DCR regulations
- Get pass/fail results

### **3. 3D Viewer**
- View generated GLB models
- Interactive controls (rotate, zoom, pan)
- Download 3D files

### **4. Feedback System**
- 👍 Positive feedback (+2 reward)
- 👎 Negative feedback (-2 reward)
- RL agent learns from feedback

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_geometry.py
```

**Test Results**: 77/82 passed (94%)

---

## 🌆 Supported Cities

| City | Authority | Rules | Status |
|------|-----------|-------|--------|
| Mumbai | MCGM | 42 | ✅ |
| Ahmedabad | AMC | 3 | ✅ |
| Pune | PMC | 4 | ✅ |
| Nashik | NMC | 4 | ✅ |

**Total**: 53 rules

---

## 🔧 Configuration

### MCP Server
- **Port**: 5001
- **Database**: MongoDB
- **Endpoints**:
  - POST `/api/mcp/save_rule`
  - GET `/api/mcp/list_rules`
  - POST `/api/mcp/feedback`
  - POST `/api/mcp/geometry`

### Environment Variables
Create `.env` file:
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=mcp_database
```

---

## 📚 Documentation

- `QUICK_START.md` - Quick reference guide
- `FRONTEND_GUIDE.md` - Frontend user guide
- `TEST_RESULTS.md` - Testing documentation
- `tests/README.md` - Test suite guide

---

## 🤝 Contributing

Contributions welcome! Please:
1. Run tests before submitting
2. Follow existing code style
3. Update documentation
4. Add tests for new features

---

## 📄 License

MIT License

---

## 🎉 Acknowledgments

Built with:
- Streamlit
- Flask
- MongoDB
- Three.js
- Trimesh
- Pytest

---

**Status**: ✅ Production Ready  
**Version**: 2.0  
**Last Updated**: November 5, 2025
