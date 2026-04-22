import streamlit as st
import sqlite3
import os
from pathlib import Path
from groq import Groq

GROQ_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_KEY:
    st.error("`$env:GROQ_API_KEY='gsk_...'`")
    st.stop()

client = Groq(api_key=GROQ_KEY)
DB_PATH = Path.cwd() / 'beko.db'

# Groq Console Models 2026
GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile", 
    "openai/gpt-oss-120b",
    "groq/compound-mini"
]

# FIXED DB - 3 columns: id, name, content
def db_init():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            content TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

db_init()  # Init tables

def db_query(sql, params=()):
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    res = conn.execute(sql, params).fetchall()
    conn.close()
    return res

def db_get(name):
    row = db_query("SELECT content FROM files WHERE name=?", (name,))
    return row[0][0] if row else ""

def db_save(name, content):
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO files (name, content) VALUES (?, ?)", (name, content))
    conn.commit()
    conn.close()

st.set_page_config(page_title="🔥 BEKO v8 - Fixed", layout="wide")

# Sidebar
with st.sidebar:
    st.header("📁 Files")
    files = [r[1] for r in db_query("SELECT id, name FROM files ORDER BY name")]
    sel = st.selectbox("File", ["New"] + files)
    
    if sel == "New":
        n = st.text_input("Name")
        c = st.text_area("Content")
        if st.button("💾"):
            db_save(n, c)
            st.success("✅")
            st.rerun()
    else:
        cnt = db_get(sel)
        edited = st.text_area("Edit", cnt, key=f"edit{sel}")
        col1, col2 = st.columns(2)
        if col1.button("💾"): 
            db_save(sel, edited)
            st.success("Updated!")
            st.rerun()
        if col2.button("🗑️"):
            db_save(sel, "")
            st.success("Deleted!")
            st.rerun()

    st.header("🤖 Model")
    model = st.selectbox("Select", GROQ_MODELS)

# Chat
st.header("🤖 BEKO v8")
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages[-6:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input()
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "DZD Ecom Arabic. Short."}
                ] + st.session_state.messages[-5:],
                max_tokens=400
            )
            response = resp.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {e}")

# Skills
with st.expander("🛠️ Skill"):
    goal = st.text_input("Goal", "Meta Ads DZD")
    if st.button("🚀"):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"SKILL.md: {goal}"}],
                max_tokens=1000
            )
            db_save("skill.md", resp.choices[0].message.content)
            st.success("✅ skill.md")
            st.code(db_get("skill.md"))
        except Exception as e:
            st.error(str(e))

st.markdown("**v8.0 Fixed Table** | Groq Console | Thread Safe")