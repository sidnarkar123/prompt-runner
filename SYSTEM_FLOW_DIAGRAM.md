# 🎯 System Flow Diagram

## Complete Data Flow Architecture

---

## 📊 Main Workflow

```mermaid
graph TD
    A[👤 User Input] -->|Enter Prompt| B[📝 Streamlit UI]
    B -->|Submit| C[🤖 Design Agent]
    C -->|Generate| D[📄 JSON Specification]
    D -->|Save| E[(specs/ folder)]
    D -->|Display| B
    
    D -->|User Checks Compliance| F[✅ Calculator Agent]
    F -->|Fetch Rules| G[(MCP Database)]
    G -->|Return Rules| F
    F -->|Calculate| H[📊 Compliance Results]
    
    F -->|Generate| I[🏗️ Geometry Converter]
    I -->|Create| J[📦 GLB File]
    J -->|Save| K[(outputs/geometry/)]
    J -->|Display| L[🎨 3D Viewer]
    
    H -->|User Feedback| M[👍👎 Feedback Buttons]
    M -->|+2 or -2| N[🧠 RL Agent]
    N -->|Store| G
    N -->|Update| O[(rl_training_logs.json)]
    
    B -->|View History| P[📂 Log Viewer]
    P -->|Load| Q[(reports/run_logs.json)]
    
    B -->|Route| R[⚡ Action Buttons]
    R -->|Send to Evaluator| S[(send_to_evaluator/)]
    R -->|Send to Unreal| T[(send_to_unreal/)]
    R -->|Log| Q
    
    style A fill:#e1f5ff
    style C fill:#fff3cd
    style F fill:#d4edda
    style I fill:#f8d7da
    style L fill:#d1ecf1
    style N fill:#e7e7ff
```

---

## 🔄 Detailed Component Flow

### 1. **Prompt Processing Flow**

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Design as Design Agent
    participant IO as IO Helpers
    participant Specs as specs/ Folder
    
    User->>UI: Enter Prompt
    UI->>Design: prompt_to_spec(prompt)
    Design->>Design: Generate JSON
    Design->>UI: Return spec_data
    UI->>IO: save_spec(spec_data)
    IO->>Specs: Write JSON file
    UI->>IO: save_prompt(prompt, filename)
    IO->>Specs: Log to prompt_logs.json
    UI->>User: Display JSON + Success Message
```

---

### 2. **Compliance Checking Flow**

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Calc as Calculator Agent
    participant MCP as MCP API
    participant DB as MongoDB
    participant Geom as Geometry Converter
    participant Files as File System
    
    User->>UI: Enter Building Parameters
    UI->>Calc: calculator_agent(city, subject)
    Calc->>MCP: GET /api/mcp/list_rules
    MCP->>DB: Query rules collection
    DB->>MCP: Return rules
    MCP->>Calc: Return filtered rules
    
    Calc->>Calc: Evaluate height, FSI, etc.
    Calc->>Geom: json_to_glb(spec_data)
    Geom->>Geom: create_building_geometry()
    Geom->>Files: Save .glb file
    
    Calc->>MCP: POST /api/mcp/geometry
    MCP->>DB: Store geometry reference
    
    Calc->>UI: Return compliance results
    UI->>User: Display Pass/Fail + 3D Model
```

---

### 3. **RL Feedback Flow**

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant MCP as MCP Server
    participant DB as MongoDB
    participant RL as RL Agent
    participant Log as Training Logs
    
    User->>UI: Click 👍 or 👎
    UI->>MCP: POST /api/mcp/feedback
    MCP->>MCP: Calculate reward (+2 or -2)
    MCP->>DB: Insert feedback document
    MCP->>DB: Insert rl_logs document
    MCP->>UI: Return success + reward
    
    RL->>MCP: Fetch feedback data
    RL->>Log: Persist training record
    Log->>Log: Update rl_training_logs.json
```

---

### 4. **3D Visualization Flow**

```mermaid
graph LR
    A[JSON Spec] -->|parse_building_spec| B[Building Parameters]
    B -->|width, height, etc| C[create_building_geometry]
    C -->|Generate Mesh| D[Trimesh Object]
    D -->|Floors| E[Ground Floor]
    D -->|Floors| F[Upper Floors]
    D -->|Boundaries| G[Setback Markers]
    D -->|Base| H[Plot Ground]
    
    E --> I[Combine Meshes]
    F --> I
    G --> I
    H --> I
    
    I -->|Apply Colors| J[Colored Mesh]
    J -->|Export| K[.GLB File]
    K -->|Display| L[Three.js Viewer]
    K -->|Download| M[User's Computer]
    
    style A fill:#fff3cd
    style C fill:#d4edda
    style L fill:#d1ecf1
```

---

## 🗂️ Data Storage Architecture

```mermaid
graph TB
    subgraph "File System"
        A[specs/]
        B[prompts/]
        C[outputs/geometry/]
        D[reports/run_logs.json]
        E[send_to_evaluator/]
        F[send_to_unreal/]
    end
    
    subgraph "MongoDB (MCP)"
        G[(rules)]
        H[(feedback)]
        I[(geometry_outputs)]
        J[(rl_logs)]
        K[(documents)]
    end
    
    subgraph "Agents"
        L[Design Agent]
        M[Calculator Agent]
        N[Geometry Converter]
        O[RL Agent]
    end
    
    L -->|Save JSON| A
    L -->|Log| D
    M -->|Query| G
    M -->|Create GLB| C
    M -->|Log geometry| I
    N -->|Generate| C
    O -->|Store rewards| J
    O -->|Store training| D
    
    style G fill:#4CAF50
    style H fill:#FFC107
    style I fill:#2196F3
    style C fill:#FF5722
    style D fill:#9C27B0
```

---

## 🔄 Multi-Agent Interaction

```mermaid
graph TD
    Start[User Request] --> Design[Design Agent]
    Design -->|JSON Spec| Storage1[(specs/)]
    
    Design --> Calculator[Calculator Agent]
    Calculator -->|Fetch| MCP[(MCP Database<br/>53 Rules)]
    MCP -->|Rules| Calculator
    
    Calculator -->|Compliance Check| Results[Results JSON]
    Calculator -->|Trigger| Geometry[Geometry Converter]
    
    Geometry -->|Building Params| Builder[Building Creator]
    Builder -->|Generate Mesh| GLB[GLB File]
    GLB -->|Save| Storage2[(outputs/geometry/)]
    
    GLB --> Viewer[3D Viewer<br/>Three.js]
    Viewer -->|Display| UI[Streamlit UI]
    
    Results --> UI
    UI -->|Feedback| RL[RL Agent]
    RL -->|Reward| MCP
    RL -->|Training Data| Storage3[(reports/)]
    
    UI -->|Route| Evaluator[Evaluator Agent]
    UI -->|Route| Unreal[Unreal Agent]
    
    style Design fill:#FFE082
    style Calculator fill:#A5D6A7
    style Geometry fill:#90CAF9
    style RL fill:#CE93D8
    style MCP fill:#FF8A65
```

---

## 🏗️ Component Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Streamlit UI<br/>main.py]
        Comp[Components<br/>glb_viewer.py, ui.py]
    end
    
    subgraph "Business Logic Layer"
        Design[Design Agent]
        Calc[Calculator Agent]
        Geom[Geometry Agent]
        RL[RL Agent]
        Parse[Parsing Agent]
        Rule[Rule Classification]
        Eval[Evaluator Agent]
        Unreal[Unreal Agent]
    end
    
    subgraph "Utility Layer"
        GeomUtil[Geometry Converter]
        IOUtil[IO Helpers]
        MCPUtil[MCP Store]
    end
    
    subgraph "Data Layer"
        MCP[MCP Server<br/>Flask API]
        Mongo[(MongoDB)]
        Files[(File System)]
    end
    
    UI --> Comp
    UI --> Design
    UI --> Calc
    UI --> RL
    
    Design --> IOUtil
    Calc --> MCPUtil
    Calc --> GeomUtil
    RL --> MCPUtil
    
    MCPUtil --> MCP
    MCP --> Mongo
    GeomUtil --> Files
    IOUtil --> Files
    
    style UI fill:#e3f2fd
    style MCP fill:#fff9c4
    style Mongo fill:#c8e6c9
```

---

## 🌆 Multi-City Data Flow

```mermaid
graph LR
    subgraph "Input"
        User[User Selects City]
    end
    
    subgraph "Cities in MCP"
        Mumbai[Mumbai<br/>42 rules]
        Ahmedabad[Ahmedabad<br/>3 rules]
        Pune[Pune<br/>4 rules]
        Nashik[Nashik<br/>4 rules]
    end
    
    subgraph "Processing"
        Filter[Calculator Agent<br/>Filters by City]
        Check[Compliance Check]
    end
    
    subgraph "Output"
        Result[Compliance Results]
        GLB[3D GLB Model]
    end
    
    User -->|Mumbai| Mumbai
    User -->|Ahmedabad| Ahmedabad
    User -->|Pune| Pune
    User -->|Nashik| Nashik
    
    Mumbai --> Filter
    Ahmedabad --> Filter
    Pune --> Filter
    Nashik --> Filter
    
    Filter --> Check
    Check --> Result
    Check --> GLB
    
    style Mumbai fill:#FF6B6B
    style Ahmedabad fill:#4ECDC4
    style Pune fill:#95E1D3
    style Nashik fill:#F38181
```

---

## 🔁 Complete System Cycle

```mermaid
flowchart TD
    Start([User Opens App]) --> Input[Enter Prompt]
    Input --> Submit{Submit?}
    Submit -->|Yes| DesignAgent[🤖 Design Agent]
    Submit -->|No| Input
    
    DesignAgent -->|Generate| JSON[📄 JSON Spec]
    JSON -->|Display| ShowJSON[Show in UI]
    JSON -->|Save| SpecFolder[(specs/)]
    
    ShowJSON --> UserChoice{User Action?}
    
    UserChoice -->|Check Compliance| CalcAgent[✅ Calculator Agent]
    UserChoice -->|Give Feedback| FeedbackBtn[👍👎 Buttons]
    UserChoice -->|View 3D| ViewerTab[🏗️ 3D Viewer Tab]
    UserChoice -->|Route| ActionBtn[⚡ Action Buttons]
    
    CalcAgent -->|Fetch Rules| MCP[(🗄️ MCP Database)]
    CalcAgent -->|Check| CompResults[Compliance Results]
    CalcAgent -->|Generate| GLBFile[📦 .GLB File]
    
    GLBFile -->|Save| GeomFolder[(outputs/geometry/)]
    GLBFile -->|Display| Viewer3D[🎨 3D Viewer]
    
    FeedbackBtn -->|+2/-2| RLAgent[🧠 RL Agent]
    RLAgent -->|Store| MCP
    RLAgent -->|Train| TrainLog[(Training Logs)]
    
    ViewerTab -->|Load GLB| GeomFolder
    ViewerTab -->|Render| Viewer3D
    
    ActionBtn -->|Copy Spec| Evaluator[(send_to_evaluator/)]
    ActionBtn -->|Copy Spec| UnrealFolder[(send_to_unreal/)]
    ActionBtn -->|Log| ActionLog[(action_logs.json)]
    
    SpecFolder -.->|Consolidate| Reports[(reports/run_logs.json)]
    ActionLog -.->|Consolidate| Reports
    TrainLog -.->|Consolidate| Reports
    
    Viewer3D --> End([User Reviews])
    CompResults --> End
    
    style Start fill:#90EE90
    style DesignAgent fill:#FFE082
    style CalcAgent fill:#A5D6A7
    style RLAgent fill:#CE93D8
    style MCP fill:#FF8A65
    style Viewer3D fill:#81D4FA
    style End fill:#90EE90
```

---

## 🎨 Frontend Component Tree

```
Streamlit App (main.py)
│
├── 📝 Prompt Input Section
│   ├── Text input box
│   ├── Submit button
│   └── Success message
│
├── 📄 JSON Specification Display
│   └── st.json() viewer
│
├── 👍👎 Feedback Section
│   ├── Good result button → +2 reward
│   └── Needs improvement → -2 reward
│
├── ✅ Compliance Checker
│   ├── City selector (4 cities)
│   ├── Building parameters input
│   │   ├── Height (m)
│   │   ├── Width (m)
│   │   ├── Depth (m)
│   │   ├── Setback (m)
│   │   └── FSI
│   ├── Check Compliance button
│   └── Results display (expandable)
│
├── 🏗️ 3D Geometry Viewer
│   ├── Tab 1: Current Model
│   │   └── Show current case GLB
│   └── Tab 2: Gallery View
│       ├── Dropdown selector
│       ├── 3D viewer (Three.js)
│       └── Download button
│
├── 📊 History Section
│   ├── Prompt Logs (left column)
│   └── Action Logs (right column)
│
└── 📂 Sidebar
    ├── Log Viewer
    │   ├── Past prompts dropdown
    │   └── JSON spec viewer
    └── Action Buttons
        ├── Send to Evaluator
        └── Send to Unreal Engine
```

---

## 🗄️ Database Schema (MongoDB)

```mermaid
erDiagram
    RULES ||--o{ FEEDBACK : "referenced by"
    RULES ||--o{ GEOMETRY_OUTPUTS : "generates"
    FEEDBACK ||--|| RL_LOGS : "creates"
    
    RULES {
        string city
        string authority
        string clause_no
        int page
        string rule_type
        string conditions
        string entitlements
        string notes
        object parsed_fields
        datetime created_at
    }
    
    FEEDBACK {
        string case_id
        object input
        object output
        string user_feedback
        int score
        datetime timestamp
    }
    
    GEOMETRY_OUTPUTS {
        string case_id
        string file_path
        object metadata
        datetime timestamp
    }
    
    RL_LOGS {
        string case_id
        int reward
        string source
        object details
        datetime timestamp
    }
```

---

## 📁 File System Structure

```
Project Root
│
├── 📝 Specifications
│   └── specs/*.json (timestamped)
│
├── 🏗️ 3D Models
│   └── outputs/geometry/*.glb
│
├── 📊 Reports (Consolidated)
│   ├── run_logs.json (unified)
│   └── backups/ (timestamped)
│
├── ⚡ Agent Routing
│   ├── send_to_evaluator/*.json
│   └── send_to_unreal/*.json
│
└── 📚 Data Storage
    └── mcp_data/rules.json (local backup)
```

---

## 🔄 Agent Communication Flow

```mermaid
flowchart LR
    subgraph "User Interface"
        UI[Streamlit<br/>main.py]
    end
    
    subgraph "Agent Layer"
        D[Design<br/>Agent]
        C[Calculator<br/>Agent]
        R[RL<br/>Agent]
        G[Geometry<br/>Converter]
    end
    
    subgraph "API Layer"
        Client[Agent<br/>Clients]
        MCP[MCP<br/>Server]
    end
    
    subgraph "Storage"
        Mongo[(MongoDB)]
        Files[(Files)]
    end
    
    UI -.->|Calls| D
    UI -.->|Calls| C
    UI -.->|Calls| R
    
    D -->|Uses| Files
    C -->|Uses| Client
    R -->|Uses| Client
    C -->|Uses| G
    
    Client -->|HTTP API| MCP
    MCP -->|CRUD| Mongo
    G -->|Writes| Files
    
    style UI fill:#E3F2FD
    style Client fill:#FFF9C4
    style MCP fill:#FFCCBC
    style Mongo fill:#C8E6C9
```

---

## 🎯 Request/Response Flow

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant ST as Streamlit
    participant DA as Design Agent
    participant CA as Calculator Agent
    participant API as MCP API
    participant DB as MongoDB
    participant GC as Geometry Converter
    participant FS as File System
    
    U->>ST: Enter "7-floor building Mumbai"
    ST->>DA: prompt_to_spec(prompt)
    DA-->>ST: JSON specification
    ST->>FS: Save to specs/
    ST->>U: Display JSON
    
    U->>ST: Click "Check Compliance"
    ST->>CA: calculator_agent("Mumbai", params)
    CA->>API: GET /api/mcp/list_rules
    API->>DB: db.rules.find({city: "Mumbai"})
    DB-->>API: 42 rules
    API-->>CA: Rules list
    
    CA->>CA: Evaluate compliance
    CA->>GC: json_to_glb(spec_data)
    GC->>GC: create_building_geometry()
    GC->>FS: Save .glb file
    GC-->>CA: glb_path
    
    CA->>API: POST /api/mcp/geometry
    API->>DB: db.geometry_outputs.insert()
    
    CA-->>ST: Compliance results + GLB path
    ST->>U: Show results + 3D model
    
    U->>ST: Click 👍
    ST->>API: POST /api/mcp/feedback
    API->>DB: db.feedback.insert()
    API->>DB: db.rl_logs.insert()
    API-->>ST: {reward: +2}
    ST->>U: "Reward +2"
```

---

## 🌐 System Network Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser<br/>:8501]
    end
    
    subgraph "Application Layer"
        Streamlit[Streamlit Server<br/>main.py<br/>Port 8501]
        MCP[MCP API Server<br/>mcp_server.py<br/>Port 5001]
    end
    
    subgraph "Data Layer"
        MongoDB[(MongoDB<br/>Port 27017)]
        FileSystem[(File System<br/>Local Disk)]
    end
    
    Browser <-->|HTTP| Streamlit
    Streamlit <-->|REST API| MCP
    MCP <-->|PyMongo| MongoDB
    Streamlit <-->|Read/Write| FileSystem
    
    style Browser fill:#E1F5FF
    style Streamlit fill:#B2DFDB
    style MCP fill:#FFCCBC
    style MongoDB fill:#C8E6C9
    style FileSystem fill:#F0F4C3
```

---

## 📊 Complete Data Lifecycle

```mermaid
stateDiagram-v2
    [*] --> UserInput: User enters prompt
    
    UserInput --> SpecGeneration: Design Agent
    SpecGeneration --> SpecStorage: Save JSON
    SpecStorage --> DisplaySpec: Show to user
    
    DisplaySpec --> ComplianceCheck: User checks compliance
    ComplianceCheck --> FetchRules: Calculator Agent
    FetchRules --> EvaluateRules: Process rules
    EvaluateRules --> GenerateGeometry: Create 3D model
    
    GenerateGeometry --> SaveGLB: Save to disk
    SaveGLB --> LogMCP: Log to MCP
    LogMCP --> Display3D: Show in viewer
    
    Display3D --> UserFeedback: User reviews
    UserFeedback --> RLProcessing: RL Agent
    RLProcessing --> UpdateMCP: Store reward
    UpdateMCP --> TrainingLog: Persist for training
    
    Display3D --> RouteAction: User routes spec
    RouteAction --> Evaluator: Send to evaluator
    RouteAction --> UnrealEngine: Send to Unreal
    
    Evaluator --> [*]
    UnrealEngine --> [*]
    TrainingLog --> [*]
```

---

## 🔐 API Endpoints Map

```
MCP Server (http://localhost:5001)
│
├── POST /api/mcp/save_rule
│   └── Input: {city, clause_no, conditions, ...}
│   └── Output: {success, inserted_id}
│
├── GET /api/mcp/list_rules?limit=100
│   └── Output: {success, count, rules: [...]}
│
├── DELETE /api/mcp/delete_rule/<rule_id>
│   └── Output: {success, deleted_count}
│
├── POST /api/mcp/feedback
│   └── Input: {case_id, feedback: "up"|"down"}
│   └── Output: {success, feedback_id, reward}
│
└── POST /api/mcp/geometry
    └── Input: {case_id, file: "path/to.glb"}
    └── Output: {success, case_id, file}
```

---

## 🧪 Testing Architecture

```mermaid
graph TD
    Tests[Test Suite<br/>82 Tests]
    
    Tests --> Unit[Unit Tests]
    Tests --> Integration[Integration Tests]
    Tests --> E2E[End-to-End Tests]
    
    Unit --> TestMCP[test_mcp.py<br/>12 tests]
    Unit --> TestAgents[test_agents.py<br/>12 tests]
    Unit --> TestGeom[test_geometry.py<br/>17 tests]
    
    Integration --> TestInt[test_integration.py<br/>10 tests]
    
    E2E --> TestFlow[Complete Workflow<br/>Tests]
    
    TestMCP -.->|Mocks| MCPServer[MCP Server]
    TestAgents -.->|Tests| Agents[All Agents]
    TestGeom -.->|Validates| GLBFiles[GLB Generation]
    TestInt -.->|Verifies| FullSystem[Complete System]
    
    style Tests fill:#CE93D8
    style Unit fill:#A5D6A7
    style Integration fill:#90CAF9
    style E2E fill:#FFAB91
```

---

## 📚 Summary

This system implements a **complete data flow** from user input to 3D visualization:

1. **User Input** → Streamlit UI
2. **AI Processing** → Design Agent (JSON)
3. **Compliance** → Calculator Agent (Rules)
4. **3D Generation** → Geometry Converter (GLB)
5. **Visualization** → Three.js Viewer
6. **Feedback** → RL Agent (Learning)
7. **Storage** → MCP + MongoDB + Files
8. **Reporting** → Consolidated logs

**All components working together seamlessly!** 🎉

---

**Created**: November 5, 2025  
**System**: DCR Compliance Platform v2.0  
**Status**: ✅ Production Ready

