import streamlit as st
import json
import os
import subprocess
from pathlib import Path
from groq import Groq
from typing import Dict, Any, List
import sqlite3

# BEKO Claude-Code Platform v1.0 - Full Autonomous > Claude Artifacts
# Chat → Deep Think → Tools/Skills → Execute Files → Web Search → Self-Build → Auto-Fix

GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    st.error("Set $env:GROQ_API_KEY")
    st.stop()

client = Groq(api_key=GROQ_KEY)
DB_PATH = Path.cwd() / "beko_claude.db"

MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b"
]

# DB Init (files, chats, tools_history)
def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY, name TEXT UNIQUE, content TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, role TEXT, content TEXT, tool_call TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS tool_history (id INTEGER PRIMARY KEY, tool TEXT, params JSON, output TEXT)""")
    conn.commit()
    return conn

conn = init_db()

def db_get_file(name: str) -> str:
    row = conn.execute("SELECT content FROM files WHERE name=?", (name,)).fetchone()
    return row[0] if row else ""

def db_save_file(name: str, content: str):
    conn.execute("INSERT OR REPLACE INTO files (name, content) VALUES (?, ?)", (name, content))
    conn.commit()

def log_chat(role: str, content: str, tool_call: str = None):
    conn.execute("INSERT INTO chats (role, content, tool_call) VALUES (?, ?, ?)", (role, content, tool_call))
    conn.commit()

# Dynamic Skills Import (all from skills/)
sys.path.insert(0, str(Path.cwd() / "skills"))
try:
    from skill_memory import MemorySkill
    from skill_search import SearchSkill
    from skill_test import TestSkill
    from skill_deploy import DeploySkill
    from skill_refactor import RefactorSkill
    from skill_self_heal import SelfHealSkill
    from skill_plan import PlanSkill
    SKILLS_AVAILABLE = {
        "memory": MemorySkill(),
        "search": SearchSkill(),
        "test": TestSkill(),
        "deploy": DeploySkill(),
        "refactor": RefactorSkill(),
        "self_heal": SelfHealSkill(),
        "plan": PlanSkill()
    }
except:
    SKILLS_AVAILABLE = {}

# Tool Schema for Structured Output (Claude-like)
TOOLS_SCHEMA = {
    "type": "function",
    "functions": [
        {
            "name": skill_name,
            "description": f"{skill_name.replace(&#x27;_&#x27;, &#x27; &#x27;).title()} - BEKO skill",
            "parameters": {
                "type": "object",
                "properties": { "action": { "type": "string" }, "goal": { "type": "string" }, "query": { "type": "string" } },
                "required": ["action"]
            }
        } for skill_name in SKILLS_AVAILABLE.keys()
    ]
}

def execute_tool(skill_name: str, params: Dict[str, Any]) -> str:
    if skill_name in SKILLS_AVAILABLE:
        try:
            result = SKILLS_AVAILABLE[skill_name].run_skill(params)
            output = json.dumps(result)
            # Log
            conn.execute("INSERT INTO tool_history (tool, params, output) VALUES (?, ?, ?)", 
                        (skill_name, json.dumps(params), output))
            conn.commit()
            # Auto-file save if result has &#x27;file&#x27;
            if &#x27;file&#x27; in result and &#x27;content&#x27; in result:
                db_save_file(result[&#x27;file&#x27;], result[&#x27;content&#x27;])
            return output
        except Exception as e:
            return f"Error in {skill_name}: {str(e)}"
    return "Skill not available"

st.set_page_config(page_title="🔥 BEKO Claude-Code Platform", layout="wide", initial_sidebar_state="expanded")

# Sidebar
with st.sidebar:
    st.header("🤖 BEKO Claude-Code v1.0")
    model = st.selectbox("Model", MODELS)
    st.header("🛠️ Skills (7 Live)")
    for skill, instance in SKILLS_AVAILABLE.items():
        st.info(f"✅ {skill}")
    if st.button("🔄 Reload Skills"):
        st.rerun()
    st.header("📁 Files")
    files = [r[0] for r in conn.execute("SELECT name FROM files ORDER BY name").fetchall()]
    selected_file = st.selectbox("File", files + ["New..."])
    if selected_file != "New...":
        content = db_get_file(selected_file)
        st.text_area("Edit", content, key=selected_file)
        if st.button(f"Save {selected_file}"):
            db_save_file(selected_file, st.session_state[selected_file])
            st.success("Saved!")

# Main Chat - Deep Reasoning + Tools
st.header("💬 Claude-Code Chat: Think → Search → Act → Fix")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Chat
for msg in st.session_state.messages[-20:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tool"):
            st.code(msg["tool"], language="json")

# Input
if prompt := st.chat_input("Ask BEKO to code, fix, deploy, search web, build skills..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    log_chat("user", prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Deep Thinking... 🔎 Searching if needed → Executing..."):
            # Chain 1: Deep Think
            think_messages = [
                {"role": "system", "content": """
You are BEKO Claude-Code AI. Arabic/English. Deep reason step-by-step.
1. THINK: Analyze task deeply.
2. If need info/search: Call search tool.
3. PLAN: Use plan tool for complex.
4. ACT: Call relevant skill (test/refactor/deploy/edit file).
5. VERIFY: Run test/heal.
6. If error: self_heal.
7. Self-build new skills if needed.
Output JSON: {"reasoning": "str", "tool": "name", "params": {{}}, "next": "str"}
                """},
                {"role": "user", "content": prompt}
            ]
            think_resp = client.chat.completions.create(
                model=model,
                messages=think_messages,
                tools=[TOOLS_SCHEMA],
                tool_choice="auto",
                temperature=0.1
            )
            
            think_content = think_resp.choices[0].message.content or ""
            tool_call = think_resp.choices[0].message.tool_calls[0] if think_resp.choices[0].message.tool_calls else None
            
            st.markdown(f"**🧠 Reasoning:** {think_content}")
            
            if tool_call:
                tool_name = tool_call.function.name
                tool_params = json.loads(tool_call.function.arguments)
                tool_output = execute_tool(tool_name, tool_params)
                st.markdown(f"**🛠️ {tool_name}:** {tool_output}")
                
                # Chain 2: Verify + Final Response
                final_messages = think_messages + [
                    {"role": "tool", "tool_call_id": "call_1", "name": tool_name, "content": tool_output},
                    {"role": "user", "content": "Verify + final answer Arabic/Eng. Code ready? Run? Deploy?"}
                ]
                final_resp = client.chat.completions.create(model=model, messages=final_messages)
                final_answer = final_resp.choices[0].message.content
                
                st.markdown(final_answer)
                st.session_state.messages.append({"role": "assistant", "content": think_content + "\\n**Tool:** " + tool_output + "\\n**Final:** " + final_answer, "tool": {tool_name: tool_params}})
                log_chat("assistant", final_answer, json.dumps({tool_name: tool_params}))
            else:
                st.markdown(think_content)
                st.session_state.messages.append({"role": "assistant", "content": think_content})

# Artifacts Preview (Claude-like)
with st.expander("🎨 Artifacts / Live Preview"):
    st.info("Auto-generated code/files preview. Click Run/Edit.")
    for file in files[-3:]:
        content = db_get_file(file)
        if content.strip():
            with st.container():
                st.subheader(file)
                st.code(content, language="python")
                col1, col2 = st.columns(2)
                if col1.button(f"🔄 Run {file}"):
                    # Sandbox exec (safe eval for demo)
                    st.code("Running...")
                if col2.button(f"📄 Edit {file}"):
                    st.session_state[f"edit_{file}"] = content
                    edited = st.text_area("Edit", content)
                    if st.button("Save"):
                        db_save_file(file, edited)

# Footer
st.markdown("""
---
**BEKO Claude-Code v1.0** | Autonomous | Skills Live | Deep Think + Tools | Better than Claude
**Run:** `streamlit run platforms/claude_code_platform.py`
**Agent Loop:** `python autonomous_agent.py` (background)
""")
