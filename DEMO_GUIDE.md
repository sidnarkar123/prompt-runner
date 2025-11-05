# 🎨 Streamlit App Demo Guide

## 🚀 App is Running!

**URL:** http://localhost:8501

---

## 🎯 What to Test

### 1. **3D Geometry Viewer** ✨ (NEW!)

Navigate to the **"🏗️ 3D Geometry Viewer"** section:

#### Tab 1: Current Model
- Shows 3D model for the current case (if available)
- Interactive 3D viewer with Three.js

#### Tab 2: Gallery View 🎨
- **Dropdown** to select from 6 existing GLB files:
  - `300d99e6.glb`
  - `428f4664.glb`
  - `6b9bbf71.glb`
  - `73c0fc46.glb`
  - `c36410dc.glb`
  - `proj_001.glb`

**3D Controls:**
- 🖱️ **Left Click + Drag**: Rotate model
- 🖱️ **Right Click + Drag**: Pan camera
- 🖱️ **Scroll Wheel**: Zoom in/out
- 📥 **Download Button**: Download GLB file

---

### 2. **Prompt Input**

- Enter a prompt (e.g., "Design a 5-story residential building")
- Click **Submit**
- View generated JSON specification
- Give feedback: 👍 Good result / 👎 Needs improvement

---

### 3. **History Section**

**Left Column: Prompt Logs**
- All previous prompts
- Timestamps
- Spec filenames

**Right Column: Action Logs**
- Actions taken (send to evaluator/unreal)
- Timestamps and details

---

### 4. **Sidebar: Log Viewer**

- Select past prompts from dropdown
- View JSON spec
- **Action Buttons:**
  - "Send to Evaluator"
  - "Send to Unreal Engine"

---

## ✅ What Should Work

### Without MCP Server:
- ✅ 3D Geometry Viewer (gallery)
- ✅ Viewing existing GLB files
- ✅ 3D controls (rotate, zoom, pan)
- ✅ Download GLB files
- ✅ Prompt input
- ✅ JSON spec display
- ❌ Feedback buttons (needs MCP)
- ❌ New geometry generation (needs MCP)

### With MCP Server:
- ✅ Everything above PLUS:
- ✅ 👍/👎 Feedback buttons
- ✅ RL reward tracking
- ✅ New geometry generation
- ✅ Multi-city rules

---

## 🎨 Expected UI Layout

```
┌─────────────────────────────────────────────────┐
│         📝 Streamlit Prompt Runner              │
├─────────────────────────────────────────────────┤
│  Prompt Input: [________________] [Submit]      │
├─────────────────────────────────────────────────┤
│  Generated JSON Specification                   │
│  { ... }                                        │
├─────────────────────────────────────────────────┤
│  Feedback: [👍 Good result] [👎 Needs impr.]    │
├─────────────────────────────────────────────────┤
│  🏗️ 3D Geometry Viewer                          │
│  ┌───────────────────────────────────────────┐ │
│  │ [📊 Current Model] [🗂️ Gallery View]     │ │
│  ├───────────────────────────────────────────┤ │
│  │                                            │ │
│  │        ╔═══════════════════╗              │ │
│  │        ║   3D BUILDING     ║              │ │
│  │        ║   VISUALIZATION   ║              │ │
│  │        ║                   ║              │ │
│  │        ╚═══════════════════╝              │ │
│  │                                            │ │
│  │  Controls:                                 │ │
│  │  🖱️ Left Click+Drag: Rotate               │ │
│  │  🖱️ Right Click+Drag: Pan                 │ │
│  │  🖱️ Scroll: Zoom                          │ │
│  │  📥 [Download GLB]                         │ │
│  └───────────────────────────────────────────┘ │
├─────────────────────────────────────────────────┤
│  History                                        │
│  ┌─────────────┬─────────────┐                 │
│  │ Prompt Logs │ Action Logs │                 │
│  └─────────────┴─────────────┘                 │
└─────────────────────────────────────────────────┘

SIDEBAR:
┌──────────────┐
│ Log Viewer   │
├──────────────┤
│ [Dropdown]   │
│              │
│ 📄 JSON Spec │
│              │
│ [Send to     │
│  Evaluator]  │
│              │
│ [Send to     │
│  Unreal]     │
└──────────────┘
```

---

## 🧪 Testing Checklist

### 3D Viewer Tests:
- [ ] Open Gallery View tab
- [ ] Select different GLB files from dropdown
- [ ] Rotate 3D model with mouse
- [ ] Zoom in/out with scroll wheel
- [ ] Pan camera with right-click drag
- [ ] Download a GLB file
- [ ] Check file size display

### Basic Functionality:
- [ ] Enter a prompt and submit
- [ ] View generated JSON
- [ ] Check prompt appears in history
- [ ] Select past prompt from sidebar
- [ ] View spec in sidebar
- [ ] Click "Send to Evaluator"
- [ ] Click "Send to Unreal"
- [ ] Verify action logged in history

---

## 🐛 Common Issues & Solutions

### Issue 1: 3D Viewer Not Loading
**Symptoms:** Black screen, "Loading 3D Model..." stuck
**Solutions:**
1. Check browser console (F12)
2. Verify GLB file exists in `outputs/geometry/`
3. Try different GLB file from dropdown
4. Refresh page (Ctrl+R)

### Issue 2: No GLB Files in Gallery
**Symptoms:** "No geometry files found yet"
**Solutions:**
1. Check `outputs/geometry/` folder has .glb files
2. Run: `python -c "from utils.geometry_converter import batch_convert_specs; batch_convert_specs()"`
3. This will convert all specs to GLB files

### Issue 3: Feedback Buttons Not Working
**Symptoms:** Error when clicking 👍/👎
**Expected:** This is normal without MCP server
**Solution:** Start MCP server (requires MongoDB)

### Issue 4: Port Already in Use
**Symptoms:** "Address already in use"
**Solutions:**
1. Close other Streamlit instances
2. Change port: `streamlit run main.py --server.port 8502`
3. Kill process: `taskkill /F /IM streamlit.exe`

---

## 📸 Screenshot Opportunities

1. **3D Viewer with Building**
   - Gallery view showing dropdown
   - 3D model rotated at interesting angle
   - Controls visible

2. **JSON Spec Display**
   - Generated specification
   - Clean formatting

3. **History Logs**
   - Multiple entries
   - Timestamps visible

4. **Complete Interface**
   - Full page with all sections
   - Shows workflow

---

## 🎯 Demo Script

### Quick Demo (2 minutes):

1. **Intro** (10 sec)
   - "This is the Streamlit Prompt Runner with 3D visualization"

2. **Show 3D Viewer** (60 sec)
   - Click "Gallery View" tab
   - Select a GLB model
   - Rotate, zoom, show controls
   - Download a file

3. **Show Workflow** (30 sec)
   - Enter prompt
   - Show generated JSON
   - Show in history

4. **Show Actions** (20 sec)
   - Send to evaluator
   - Send to Unreal
   - Show action logs

### Full Demo (5 minutes):

1. Overview of interface
2. Explain prompt → JSON workflow
3. Deep dive into 3D viewer
4. Show all 6 GLB models
5. Demonstrate controls
6. Show history and logs
7. Explain feedback system
8. Show action routing

---

## 💡 Cool Things to Show

1. **Responsive 3D Viewer**
   - Smooth rotation
   - Real-time rendering
   - Three.js powered

2. **Multiple Building Models**
   - Different geometries
   - Various scales
   - 6 pre-generated models

3. **Complete Workflow**
   - Prompt → Spec → Geometry → Visualization
   - Full traceability

4. **Routing System**
   - Send to different agents
   - Action logging
   - Timestamp tracking

---

## 🚀 Next Steps

### To Enable Full Functionality:

1. **Install MongoDB**
   ```bash
   # Windows (using Chocolatey)
   choco install mongodb

   # Or download from: https://www.mongodb.com/try/download/community
   ```

2. **Start MongoDB**
   ```bash
   mongod
   ```

3. **Start MCP Server**
   ```bash
   cd "C:\prompt runner\streamlit-prompt-runner"
   python mcp_server.py
   ```

4. **Upload Rules**
   ```bash
   python upload_rules.py
   ```

5. **Test Full System**
   - Feedback buttons will work
   - New geometry generation will work
   - Multi-city rules will be available

---

## ✅ Success Criteria

**Minimum (Without MCP):**
- ✅ 3D viewer displays models
- ✅ Can interact with 3D models
- ✅ Can download GLB files
- ✅ Prompt input works
- ✅ JSON display works
- ✅ History logs work

**Full (With MCP):**
- ✅ All above PLUS
- ✅ Feedback system functional
- ✅ Real-time geometry generation
- ✅ 4 cities with rules
- ✅ RL reward tracking

---

**Enjoy testing your app!** 🎉

**App URL:** http://localhost:8501

