# Vantaguard 🛡️

> **Architectural Intelligence. Autonomous Assurance.**

Vantaguard is an advanced, AI-powered security auditing platform designed to autonomously analyze, verify, and report vulnerabilities in software repositories. Built on a multi-agent architecture, it bridges the gap between static code analysis and dynamic execution by utilizing isolated Docker sandboxes to actively test potential exploits before flagging them.

---

# 📖 Overview

Traditional Static Application Security Testing (SAST) tools often generate high volumes of false positives. Vantaguard addresses this limitation through a stateful LangGraph-powered multi-agent pipeline that not only identifies vulnerabilities but actively attempts to verify them in isolated execution environments.

The platform clones repositories, maps architecture, formulates exploit hypotheses, dynamically installs dependencies inside secure containers, executes generated proof-of-concept verification scripts, and compiles professional audit reports with contextual conversational memory.

---

# ✨ Key Features

## 🤖 Multi-Agent Workflow

Vantaguard utilizes specialized AI agents to decompose the security auditing lifecycle into highly focused stages:

- **Router**
- **Mapper**
- **Attacker**
- **Verifier**
- **Reporter**
- **Aligner**
- **Assistant**

This architecture significantly improves reasoning precision and audit reliability.

---

## 🧪 Dynamic Sandbox Verification

Instead of relying purely on static analysis:

- Required Python dependencies are extracted automatically
- Missing modules are dynamically installed
- Exploit verification scripts are executed securely
- Verification happens inside an isolated non-root Docker sandbox

This dramatically reduces false positives.

---

## 🧠 Contextual Conversational Memory

Persistent conversational state enables:

- Follow-up questions on prior audits
- Context-aware vulnerability discussions
- Multi-turn reasoning over repositories
- Continuous audit conversations across sessions

---

## 🔄 Intelligent Routing & Recovery

Vantaguard intelligently distinguishes between:

- Conversational requests
- Audit requests
- Invalid or incomplete user prompts

The assistant gracefully recovers from missing repository URLs, empty repositories, invalid targets, and unsupported workflows.

---

## 🧹 Automated Resource Management

The system includes a robust cleanup pipeline that:

- Removes temporary Git clones
- Clears execution artifacts
- Prevents resource leakage
- Maintains OS-agnostic compatibility

---

## 🔐 Secure Authentication

Authentication infrastructure includes:

- Session-based authentication
- Password hashing
- MongoDB-backed persistence
- User-specific audit history

---

# 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | FastAPI, Python 3.11 |
| **AI Orchestration** | LangGraph, LangChain |
| **LLM Providers** | Groq, Gemini |
| **Execution Environment** | Docker Sandbox |
| **Database** | MongoDB |
| **Frontend** | Streamlit |
| **Authentication** | Session Middleware + Password Hashing |

---

# 🧩 System Architecture

Vantaguard operates using a stateful graph-based execution pipeline.

---

## 1️⃣ Router Agent

Analyzes user intent and determines whether the request should:

- Trigger the audit pipeline
- Enter conversational assistant mode

---

## 2️⃣ Mapper Agent

Responsible for:

- Cloning repositories
- Extracting codebases
- Identifying attack surfaces
- Detecting sources and sinks

---

## 3️⃣ Attacker Agent

Generates exploit hypotheses based on:

- Repository architecture
- Data flow analysis
- Security anti-patterns
- Misconfigurations

---

## 4️⃣ Verifier Agent

The Verifier dynamically:

- Generates executable verification scripts
- Extracts external dependencies
- Installs missing packages inside the sandbox
- Executes proof-of-concept exploit code
- Captures `stdout`, `stderr`, and execution traces

---

## 5️⃣ Reporter Agent

Compiles raw findings into structured vulnerability logs.

---

## 6️⃣ Aligner Agent

Transforms raw findings into:

- Human-readable reports
- Professional security documentation
- Structured remediation guidance

---

## 7️⃣ Assistant Agent

Handles:

- Follow-up questions
- Audit discussions
- Contextual explanations
- Recovery from invalid inputs

---

# ⚙️ Installation & Setup

## 📌 Prerequisites

Ensure the following are installed:

- Python 3.11+
- Docker Desktop
- MongoDB (Local or Atlas)
- Groq API Key
- Gemini API Key

---

# 🚀 Setup Instructions

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/AkshayKapoor024/vantaguard.git

cd vantaguard
```

## 2️⃣ Configure Environment Variables

Create a `.env` file in the root directory and add the required environment variables:

```env
SESSION_SECRET_KEY=your_secure_session_key

MONGO_URI=your_mongodb_connection_string

GROQ_API_KEY=your_groq_api_key

GOOGLE_API_KEY=your_google_api_key

BACKEND_URL=http://localhost:8080
```

## 2️⃣ Configure Environment Variables

Build the isolated Docker sandbox used for secure code verification:

```bash
cd sandbox

docker build -t vantaguard-sandbox .
```

## 4️⃣ Run the Sandbox Container

Start the sandbox container with DNS configuration for stable package installation and internet resolution:

```bash
docker run -d \
  --name sandbox \
  --dns 8.8.8.8 \
  --dns 1.1.1.1 \
  vantaguard-sandbox
```

## 5️⃣ Pre-Install Common Verification Libraries (Optional but Recommended)

To reduce repeated package installation time during verification:

```bash
docker exec sandbox python3 -m pip install --user \
requests \
beautifulsoup4 \
lxml \
pyyaml \
python-dotenv \
flask \
fastapi \
uvicorn \
aiohttp \
httpx \
cryptography \
pyjwt \
bcrypt \
passlib \
markdown \
bleach \
dill \
joblib
```

## 6️⃣ Start the FastAPI Backend

Launch the FastAPI backend server:

```bash
uvicorn server.main:app --host 0.0.0.0 --port 8080
```

## 7️⃣ Start the Streamlit Frontend

Open a new terminal and launch the Streamlit frontend:

```bash
streamlit run client/app.py
```

## 🎯 Usage Examples
### 🔍 Triggering a Security Audit

Provide a valid GitHub repository URL with an auditing directive:

Audit this repository:

```bash
https://github.com/username/project
```

Check for broken access controls.

### 💬 Contextual Follow-Up Conversations

Leverage conversational memory without re-uploading the repository:
```bash
Tell me more about the SQL injection vulnerability found in db_manager.py.
Why is it critical?
```

### 🛡️ Testing the Fail-Safe Recovery Logic

Attempt an audit without providing a repository URL:

```bash
Can you scan my project for security flaws?
```

The assistant intelligently detects the missing repository and requests the required GitHub URL before starting the audit pipeline.

## 📂 Additional Highlights

### ✅ Dynamic Dependency Resolution

The verifier automatically:

- Extracts imported Python modules
- Detects missing dependencies
- Installs required packages dynamically
- Reuses already-installed packages inside the sandbox

### ✅ Persistent Conversational State

Vantaguard maintains contextual memory using:

MongoDB-backed chat histories
LangGraph state reconstruction
Session-based conversational continuity

### ✅ Secure Sandbox Architecture

Verification executes inside:

Non-root isolated Docker containers
Ephemeral execution environments
Dynamically managed runtime sandboxes

This ensures safe exploit validation without exposing the host machine.

## 👨‍💻 Developer

**Developed by Akshay Kapoor.**

Vantaguard represents a high-level integration of:

- Multi-Agent AI Architectures
- Stateful LangGraph Orchestration
- Autonomous Security Verification
- Dynamic Sandbox Execution
- Cloud-Native Security Automation

## 📜 License & Disclaimer

This project is intended strictly for:

- Educational purposes
- Defensive security research
- Responsible vulnerability analysis
- Authorized repository auditing

**Do not use this platform against systems you do not own or have explicit permission to assess.**

# 🛡️ Vantaguard

***Architectural Intelligence. Autonomous Assurance***