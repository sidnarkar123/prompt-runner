# 🎨 Frontend User Guide

## Complete Multi-Agent Interface

**Location**: `main.py`  
**Access**: http://localhost:8501

---

## 🎯 5 Main Tabs

### 1. 🎨 **Design Studio**
**Purpose**: Create building specifications from natural language

**Features**:
- ✅ Text prompt input
- ✅ AI-powered spec generation
- ✅ Quick templates
- ✅ Instant feedback (👍/👎)
- ✅ JSON specification display

**How to Use**:
1. Enter description: "7-story residential building in Mumbai"
2. Click **Generate Spec**
3. Review JSON output
4. Provide feedback

---

### 2. ✅ **Compliance Checker**
**Purpose**: Check building compliance against DCR regulations

**Features**:
- ✅ Multi-city support (Mumbai, Ahmedabad, Pune, Nashik)
- ✅ Manual or spec-based input
- ✅ Real-time compliance checking
- ✅ Detailed rule breakdown
- ✅ Pass/fail indicators

**How to Use**:
1. Select city
2. Choose input method:
   - Use current spec, OR
   - Enter parameters manually
3. Click **Check Compliance**
4. Review results for each rule

**Parameters**:
- Height (m)
- Width (m)
- Depth (m)
- Setback (m)
- FSI/FAR
- Building type

---

### 3. 🏗️ **3D Viewer**
**Purpose**: Interactive 3D building visualization

**3 Sub-tabs**:

#### a) **Current Model**
- View 3D model of current design
- Download GLB file
- Generate model if missing

#### b) **Gallery**
- Browse all generated models
- Interactive 3D controls:
  - 🖱️ Left drag: Rotate
  - 🖱️ Right drag: Pan
  - 🖱️ Scroll: Zoom
- Download any model

#### c) **Generate New**
- Custom model creator
- Slider controls for dimensions
- Real-time parameters:
  - Width, Depth, Height
  - Setback
  - Number of floors
  - Building type
  - Compliance status
- Instant 3D preview

---

### 4. 📊 **Rule Explorer**
**Purpose**: Search and explore DCR regulations

**Features**:
- ✅ Multi-city search
- ✅ Filter by building type
- ✅ Detailed rule information
- ✅ Conditions & entitlements
- ✅ Notes and references

**How to Use**:
1. Select cities to search
2. Select building types
3. Click **Search Rules**
4. Browse results
5. Expand for details

---

### 5. 📈 **Analytics**
**Purpose**: System usage statistics and performance

**Metrics**:
- Total prompts processed
- Total actions taken
- 3D models generated
- Specifications created

**Views**:
- Recent prompts table
- Recent actions table
- Real-time activity feed

---

## 🎛️ **Sidebar Control Panel**

### **System Status** 📡
- MCP Server status
- MongoDB connection status
- Real-time health check

### **Past Projects** 📂
- Browse previous designs
- Load any project
- View specifications
- One-click project restore

### **Quick Actions** ⚡
- Send to Evaluator
- Send to Unreal Engine
- Export specifications

---

## 🚀 **Quick Start Workflow**

### **Complete Project Flow**:

```
1. DESIGN STUDIO Tab
   ↓
   Enter: "5-story residential Mumbai"
   Click: Generate Spec
   ↓
2. COMPLIANCE CHECKER Tab
   ↓
   Select: Mumbai
   Click: Check Compliance
   Review: Pass/Fail results
   ↓
3. 3D VIEWER Tab
   ↓
   View: Current Model
   Or Generate: Custom model
   Download: GLB file
   ↓
4. Provide Feedback
   ↓
   👍 or 👎
```

---

## 💡 **Tips & Tricks**

### **Design Studio**:
- Be specific in prompts
- Include city, type, floors
- Mention setback & FSI if known

### **Compliance Checker**:
- Check multiple cities
- Review all rule details
- Note non-compliant items

### **3D Viewer**:
- Use Custom Generator for quick tests
- Download models for external use
- Try different building types

### **Rule Explorer**:
- Use multiple filters
- Browse all available rules
- Find specific requirements

---

## 🎨 **Available Agents**

### **Active in Frontend**:

1. ✅ **Design Agent**
   - Tab: Design Studio
   - Function: Generate specs from prompts

2. ✅ **Calculator Agent**
   - Tab: Compliance Checker
   - Function: Check DCR compliance

3. ✅ **Geometry Converter**
   - Tab: 3D Viewer
   - Function: Generate GLB models

4. ✅ **RL Agent** (Background)
   - Location: Feedback buttons
   - Function: Learn from feedback

5. ✅ **MCP Client** (Background)
   - Location: All tabs
   - Function: Database operations

---

## 🔧 **Troubleshooting**

### **"MCP Server Offline"**
**Solution**: 
```bash
python mcp_server.py
```

### **"MongoDB Not Connected"**
**Solution**: Check MongoDB is running

### **"No 3D Model Available"**
**Solution**: Click "Generate 3D Model Now" button

### **"Compliance Check Failed"**
**Solution**: Ensure MCP server has rules loaded

---

## 📊 **Features Summary**

| Feature | Tab | Status |
|---------|-----|--------|
| Prompt → Spec | Design Studio | ✅ |
| Compliance Check | Compliance | ✅ |
| 3D Viewing | 3D Viewer | ✅ |
| 3D Generation | 3D Viewer | ✅ |
| Rule Search | Rule Explorer | ✅ |
| Analytics | Analytics | ✅ |
| Feedback System | All | ✅ |
| Project History | Sidebar | ✅ |
| Multi-City | All | ✅ |

---

## 🎯 **Example Use Cases**

### **Case 1: New Project**
1. Go to **Design Studio**
2. Enter: "8-floor commercial building in Pune with parking"
3. Generate spec
4. Check compliance in **Compliance Checker**
5. View 3D model in **3D Viewer**

### **Case 2: Compliance Check**
1. Go to **Compliance Checker**
2. Select city: Mumbai
3. Enter manual parameters
4. Check against all rules
5. Review compliance status

### **Case 3: Explore Regulations**
1. Go to **Rule Explorer**
2. Select: Pune + Residential
3. Browse available rules
4. Note requirements

### **Case 4: Custom 3D Model**
1. Go to **3D Viewer** → Generate New
2. Adjust sliders for dimensions
3. Set building type
4. Generate model
5. Download GLB

---

## 🌟 **Advanced Features**

### **Session State**:
- Persistent current design
- Auto-save specifications
- Cross-tab data sharing

### **Real-time Updates**:
- Instant compliance results
- Live 3D rendering
- Dynamic analytics

### **Error Handling**:
- Graceful MCP failures
- User-friendly messages
- Fallback options

---

## 📱 **Interface Layout**

```
┌─────────────────────────────────────────┐
│  🏗️ DCR Compliance System              │
├─────────────────────────────────────────┤
│ [Design] [Compliance] [3D] [Rules] [...] │
├─────────────────────────────────────────┤
│                                         │
│         ACTIVE TAB CONTENT              │
│                                         │
│         (Changes based on tab)          │
│                                         │
├─────────────────────────────────────────┤
│  Feedback | Analytics | History         │
└─────────────────────────────────────────┘

SIDEBAR:
┌──────────┐
│ Status   │
│ Projects │
│ Actions  │
└──────────┘
```

---

## 🎊 **What's New**

### **v2.0 Features**:
- ✅ 5 organized tabs
- ✅ Custom 3D generator
- ✅ Rule explorer
- ✅ Real-time analytics
- ✅ System status indicators
- ✅ One-click project loading
- ✅ Enhanced error handling
- ✅ Better UI/UX

---

## 🚀 **Getting Started**

```bash
# 1. Start MCP Server
python mcp_server.py

# 2. Start Streamlit
streamlit run main.py

# 3. Open browser
http://localhost:8501

# 4. Start designing!
```

---

**Your complete multi-agent platform is ready!** 🎉

All agents are integrated and accessible through the beautiful new interface!


