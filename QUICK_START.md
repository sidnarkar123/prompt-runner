# ⚡ QUICK START GUIDE

## 🚀 Start the System (2 Steps)

### **Step 1: Start MCP Server**
```bash
cd "C:\prompt runner\streamlit-prompt-runner"
python mcp_server.py
```
✅ Wait for: "Running on http://0.0.0.0:5001"

### **Step 2: Start Streamlit App**
```bash
# New terminal
cd "C:\prompt runner\streamlit-prompt-runner"
streamlit run main.py
```
✅ Opens browser automatically at: http://localhost:8501

---

## 📊 System Status Check

```bash
# Check MCP Server
curl http://127.0.0.1:5001/

# Check MongoDB
mongo --eval "db.adminCommand('ping')"

# Run Tests
pytest
```

---

## 🎯 Common Commands

### **Upload City Rules:**
```bash
python upload_rules.py
```

### **Run Tests:**
```bash
pytest                    # All tests
pytest -v                 # Verbose
pytest --cov=.            # With coverage
```

### **Generate GLB Files:**
```bash
python -c "from utils.geometry_converter import batch_convert_specs; batch_convert_specs()"
```

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 5001 in use | `taskkill /F /PID <pid>` |
| MongoDB not connecting | Check `mongod` is running |
| Tests failing | Start MCP server first |
| 3D viewer blank | Check `.glb` files in `outputs/geometry/` |

---

## 📁 Key Files

- **Main App**: `main.py`
- **MCP Server**: `mcp_server.py`
- **Rules**: `mcp_data/rules.json`
- **3D Viewer**: `components/glb_viewer.py`
- **Tests**: `tests/`

---

## ✅ What Works

✅ 3D Geometry Viewer  
✅ Compliance Checker  
✅ Feedback System (👍/👎)  
✅ 4 Cities (53 rules)  
✅ RL Rewards (+2/-2)  
✅ 82 Tests (94% pass)

---

## 🎯 URLs

- **Streamlit**: http://localhost:8501
- **MCP API**: http://localhost:5001
- **MongoDB**: mongodb://localhost:27017

---

**Quick Start Complete!** 🚀
