# 🤖 AI Multi-Agent Job Assistant

An AI-powered multi-agent job assistant that helps job seekers analyze their resumes, identify skill gaps, match their resume with job descriptions, rewrite their resumes, and prepare for interviews.

Built using **Python, Streamlit, LangGraph, and Google Gemini**.

---

## 🚀 Features

### 📄 Resume Analysis

* Upload a PDF resume
* Extract resume content
* Analyze resume quality
* Calculate ATS score
* Identify strengths and weaknesses

### ✨ Resume Rewrite

* Improve resume content
* Rewrite weak sections
* Make resume more ATS-friendly
* Generate stronger professional descriptions

### 🎯 Skill Gap Analysis

* Identify missing skills
* Compare current skills with target role requirements
* Recommend skills to learn

### 📊 Job Matching

* Match resume with a Job Description
* Calculate job compatibility
* Identify matching and missing skills

### 💬 Interview Preparation

* Generate role-specific interview questions
* Prepare technical questions
* Prepare HR questions
* Help candidates practice for interviews

### 📘 Final Report

* Combine results from multiple AI agents
* Provide a complete career-readiness report

---

## 🧠 Multi-Agent Architecture

The application uses **LangGraph** to coordinate multiple specialized AI agents.

```text
                    ┌─────────────────┐
                    │  User Resume    │
                    │ + Job Description│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Planner Agent  │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
 ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
 │ Resume Agent   │  │ Skill Gap Agent│  │ Job Match Agent│
 └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Resume Rewrite  │
                    │     Agent       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Interview Agent │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Final Report   │
                    │     Agent       │
                    └─────────────────┘
```

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **LangGraph**
* **Google Gemini**
* **python-dotenv**
* **PDF text extraction**
* **Git & GitHub**

---

## 📂 Project Structure

```text
ai_multi_agent_job_assistant/
│
├── agents/
│   ├── planner.py
│   ├── resume_agent.py
│   ├── skill_agent.py
│   ├── job_match_agent.py
│   ├── interview_agent.py
│   ├── resume_rewrite_agent.py
│   └── final_agent.py
│
├── streamlit_app.py
├── graph.py
├── state.py
├── llm.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .env
```

> **Note:** `.env` contains private API credentials and should never be committed to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-multi-agent-job-assistant.git
```

### 2. Open the project

```bash
cd ai-multi-agent-job-assistant
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

### Windows

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

Never upload your `.env` file to GitHub.

---

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

---

## 🖥️ Application Workflow

```text
Upload Resume
      ↓
Resume Analysis
      ↓
ATS Score
      ↓
Skill Gap Analysis
      ↓
Job Description Matching
      ↓
Resume Rewrite
      ↓
Interview Questions
      ↓
Final Career Report
```

---

## 📊 Example Dashboard

The application provides:

| Feature        | Result                      |
| -------------- | --------------------------- |
| ATS Score      | Resume compatibility score  |
| Skill Match    | Skills matching target role |
| JD Match       | Resume vs Job Description   |
| Missing Skills | Skills to improve           |
| Resume Rewrite | Improved resume content     |
| Interview      | Role-specific questions     |
| Final Report   | Overall career analysis     |

---

## ☁️ Streamlit Cloud Deployment

The application can be deployed using **Streamlit Community Cloud**.

### Steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select `streamlit_app.py` as the main file.
5. Add your Gemini API key under Streamlit Secrets.

Example:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

6. Deploy the application.

---

## 🔐 Security

Do not commit sensitive files such as:

```text
.env
```

Add them to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

If an API key is accidentally exposed, revoke it and create a new key.

---

## 🎯 Future Improvements

* LinkedIn job search integration
* Automated job recommendations
* Resume DOCX/PDF generation
* Voice-based interview practice
* Interview performance scoring
* Personalized learning roadmap
* Job application tracking
* Email-based job alerts
* RAG-based career knowledge assistant

---

## 👩‍💻 Author

**Keerthana P**

AI Engineer | Python | GenAI | LangGraph | Streamlit

---

## ⭐ Project Goal

The goal of this project is to build an intelligent AI career assistant that can guide candidates from **resume preparation to interview preparation** using a multi-agent architecture.
