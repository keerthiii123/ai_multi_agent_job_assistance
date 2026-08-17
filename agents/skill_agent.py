from state import AgentState
import re

# ==========================================
# ROLE SKILLS
# ==========================================

ROLE_SKILLS = {
    "AI Engineer": [
        "python","langchain","langgraph","rag",
        "chromadb","fastapi","huggingface",
        "embeddings","vector database","llm",
        "generative ai","gemini","groq",
        "git","github","streamlit","docker"
    ]
}

# ==========================================
# ALIASES
# ==========================================

ALIASES = {

    "python":[
        "python","python programming","python3","pyth on"
    ],

    "langchain":[
        "langchain","lang chain"
    ],

    "langgraph":[
        "langgraph","lang graph","langgr aph"
    ],

    "rag":[
        "rag",
        "r a g",
        "retrieval augmented generation",
        "retrieval-augmented generation",
        "rag pipeline",
        "rag pipelines"
    ],

    "chromadb":[
        "chromadb","chroma db","chroma"
    ],

    "fastapi":[
        "fastapi","fast api","f ast api"
    ],

    "huggingface":[
        "huggingface",
        "hugging face",
        "sentence-transformers",
        "sentence transformers"
    ],

    "embeddings":[
        "embedding",
        "embeddings",
        "embedding model",
        "sentence-transformers"
    ],

    "vector database":[
        "vector database",
        "vector databases",
        "vector db",
        "chromadb",
        "faiss",
        "pinecone",
        "weaviate",
        "qdrant",
        "pgvector"
    ],

    "llm":[
        "llm","llms",
        "large language model",
        "large language models"
    ],

    "generative ai":[
        "generative ai",
        "genai",
        "gen ai"
    ],

    "gemini":[
        "gemini",
        "google gemini",
        "gemini api"
    ],

    "groq":[
        "groq","groq api","gr oq"
    ],

    "streamlit":[
        "streamlit","str eamlit"
    ],

    "docker":[
        "docker","dockerfile",
        "containerization",
        "containerized"
    ],

    "git":["git"],

    "github":[
        "github","github.com","git hub"
    ]
}

# ==========================================
# NORMALIZE
# ==========================================

def normalize(text: str):

    if not text:
        return ""

    text = text.lower()

    text = text.replace("-", " ")
    text = text.replace("_", " ")
    text = text.replace("/", " ")

    # Join spaced letters
    text = re.sub(
        r'\b(?:[a-z]\s+){2,}[a-z]\b',
        lambda m:m.group(0).replace(" ",""),
        text
    )

    replacements = {
        "langgr aph":"langgraph",
        "lang graph":"langgraph",
        "r a g":"rag",
        "hugging face":"huggingface",
        "str eamlit":"streamlit",
        "gr oq":"groq",
        "f ast api":"fastapi",
        "chroma db":"chromadb",
        "git hub":"github",
        "pyth on":"python"
    }

    for old,new in replacements.items():
        text=text.replace(old,new)

    text=re.sub(r"\s+"," ",text)

    return text.strip()

# ==========================================
# SKILL CHECK
# ==========================================

def skill_found(text,skill):

    text=normalize(text)

    keywords=ALIASES.get(skill,[skill])

    for keyword in keywords:

        keyword=normalize(keyword)

        pattern=rf"(?<!\w){re.escape(keyword)}(?!\w)"

        if re.search(pattern,text):
            return True

    return False

# ==========================================
# FIND SKILLS
# ==========================================

def find_skills(text,skills):

    return [
        skill
        for skill in skills
        if skill_found(text,skill)
    ]

# ==========================================
# FORMAT
# ==========================================

def format_skills(skills):

    if not skills:
        return "None"

    return "\n".join(
        f"✓ {s.title()}"
        for s in skills
    )

# ==========================================
# AGENT
# ==========================================

def skill_agent(state:AgentState):

    resume=normalize(state.get("resume_text",""))
    jd=normalize(state.get("job_description",""))
    role=state.get("target_role","AI Engineer")

    skills=ROLE_SKILLS.get(role)

    if not skills:

        return {
            "skill_gap":"No mapping available."
        }

    existing=find_skills(resume,skills)

    # Gemini optional
    optional={"gemini"}

    missing=[
        s
        for s in skills
        if s not in existing and s not in optional
    ]

    jd_required=find_skills(jd,skills)

    jd_missing=[
        s
        for s in jd_required
        if s not in existing
    ]

    role_score=round(len(existing)/len(skills)*100)

    jd_score=(
        round((len(jd_required)-len(jd_missing))/len(jd_required)*100)
        if jd_required else 0
    )

    priority=jd_missing or missing[:5]

    report=f"""
## 🎯 Skill Gap Analysis

### Target Role

**{role}**

---

### 📊 Overall Role Skill Match

**{role_score}%**
"""

    if jd_required:
        report+=f"""

### 📋 Job Description Skill Match

**{jd_score}%**
"""

    report+=f"""

---

### ✅ Skills Found in Resume

{format_skills(existing)}

---

### ❌ Missing Skills

"""

    if missing:
        report+="\n".join(f"✗ {s.title()}" for s in missing)
    else:
        report+="No major skills missing."

    report+=f"""

---

### 🔥 High Priority Skill Gaps

"""

    if priority:
        report+="\n".join(f"🔥 {s.title()}" for s in priority)
    else:
        report+="None"

    report+=f"""

---

### 📚 Recommended Learning Order

"""

    for i,s in enumerate(priority,1):
        report+=f"\n{i}. {s.title()}"

    report+=f"""

---

### 🔍 Skill Detection Summary

Role skills checked: **{len(skills)}**

Skills found: **{len(existing)}**

Skills missing: **{len(missing)}**
"""

    if jd_required:
        report+=f"""

JD skills detected: **{len(jd_required)}**

JD skills missing: **{len(jd_missing)}**
"""

    return {"skill_gap":report}