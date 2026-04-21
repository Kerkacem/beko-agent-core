import streamlit as st
import os
from groq import Groq
import sqlite3
from pathlib import Path

# API Key من ENV (آمن)
GROQ_KEY = os.getenv('GROQ_API_KEY')
if not GROQ_KEY or 'gsk' not in GROQ_KEY:
    st.error("""
    🚨 خطأ: ضع API Key أولاً:
    ```
    $env:GROQ_API_KEY="gsk_your_full_key_here"
    ```
    ثم أعد التشغيل.
    """)
    st.stop()

client = Groq(api_key=GROQ_KEY)
DB_PATH = Path.cwd() / 'beko.db'

# DB
@st.cache_resource
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files 
                 (id INTEGER PRIMARY KEY, name TEXT UNIQUE, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chats 
                 (id INTEGER PRIMARY KEY, message TEXT, response TEXT)''')
    conn.commit()
    return conn

conn = init_db()

st.set_page_config(page_title="🔥 BEKO AI Platform v2.0", layout="wide")

# Sidebar
st.sidebar.header("📁 الملفات")
files = conn.execute("SELECT name FROM files ORDER BY name").fetchall()
file_list = [f[0] for f in files] or ["لا ملفات"]
selected = st.sidebar.selectbox("اختر", file_list)

if selected != "لا ملفات":
    data = conn.execute("SELECT content FROM files WHERE name=?", (selected,)).fetchone()
    st.sidebar.text_area("المحتوى", data[0] if data else "", height=150)

st.sidebar.header("➕ جديد")
new_name = st.sidebar.text_input("الاسم")
new_content = st.sidebar.text_area("المحتوى", height=100)
if st.sidebar.button("💾 حفظ", type="primary"):
    conn.execute("INSERT OR REPLACE INTO files VALUES ((SELECT COALESCE(MAX(id)+1,1) FROM files),?,?)", 
                (new_name, new_content))
    conn.commit()
    st.sidebar.success("✅ محفوظ!")
    st.rerun()

# Chat
st.header("🤖 BEKO AI - كامل مثل Claude Code")
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("💭 اكتب...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("⏳ يفكر..."):
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Belkacem Meta Ads Manager DZD COD. عربي."}] + 
                        st.session_state.messages[-8:]
            )
            resp_text = resp.choices[0].message.content
            st.markdown(resp_text)
            st.session_state.messages.append({"role": "assistant", "content": resp_text})
    
    conn.execute("INSERT INTO chats (message, response) VALUES (?, ?)", (prompt, resp_text))
    conn.commit()

# Skills
with st.expander("🛠️ بناء Skill"):
    skill_goal = st.text_area("وصف المهارة", "Meta Ads DZD generator")
    if st.button("🚀 أنشئ", type="primary"):
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "أنشئ SKILL.md كامل."}, {"role": "user", "content": skill_goal}]
        )
        skill = resp.choices[0].message.content
        conn.execute("INSERT OR REPLACE INTO files (name, content) VALUES (?, ?)", ("skill.md", skill))
        conn.commit()
        st.success("✅ skill.md محفوظ!")
        st.code(skill, language="markdown")

st.markdown("---")
st.caption("**v2.0** | DZD Ecom | http://localhost:8501")