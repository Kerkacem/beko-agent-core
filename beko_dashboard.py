import streamlit as st
import json
import os
from pathlib import Path

st.set_page_config(page_title="BEKO Marketing Master", layout="wide")
st.title("🚀 MARKETING MASTER ENGINE v1.0")
st.markdown("### بلكاسم - مدير إعلانات Meta + Ecom DZ")

# Sidebar
st.sidebar.title("الأوامر")
command = st.sidebar.selectbox("اختر أمر:", [
    "RUN FULL PRODUCT INTELLIGENCE REPORT",
    "BUILD CAMPAIGN STRUCTURE", 
    "RUN SALES MASTERY UNIT",
    "BUILD HONEYPOT",
    "ANALYZE METRICS",
    "SCALE CAMPAIGN"
])

product = st.sidebar.text_input("اسم المنتج (حقائب جلدية)", "حقائب جلدية")
budget = st.sidebar.number_input("الميزانية DZD", 1000, 10000, 5000)

if st.sidebar.button("🚀 نفّذ الأمر"):
    goal = f"{command} {product} {budget} DZD act_4330803053874384"
    
    # Write goal
    Path("goal.txt").write_text(goal)
    
    # Run BEKO
    os.system("python beko-agent-main.py")
    
    # Show results
    if Path("plan.json").exists():
        with open("plan.json", "r", encoding="utf-8") as f:
            plan = json.load(f)
        st.success("تم! 📊")
        st.json(plan)
    
    st.balloons()

# Main dashboard
col1, col2 = st.columns(2)
with col1:
    st.header("📈 KPIs حالية")
    st.metric("ROAS", "2.8x")
    st.metric("TRC", "25%")
    st.metric("CPA", "120 DZD")
    
with col2:
    st.header("💰 Campaign Status")
    st.metric("Spend", "5000 DZD")
    st.metric("Sales", "14000 DZD")
    st.metric("Return", "30%")

st.header("📱 APIs جاهزة")
st.code("""
Status: iwr http://127.0.0.1:5000/status -UseBasicParsing
Register: $body=@{username='test';password='123'}|ConvertTo-Json; iwr ...
""", language="powershell")