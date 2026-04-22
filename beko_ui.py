import streamlit as st
import subprocess
import json
from pathlib import Path

st.set_page_config(layout="wide")
st.title("🎯 BEKO - مدير إعلانات Meta")
st.markdown("---")

# الأوامر
col1, col2 = st.columns([2,1])
with col1:
    st.header("الأمر")
    command = st.selectbox("", ["تحليل منتج", "بناء حملة", "سكريبتات بيع", "حلل البيانات"])
with col2:
    st.header("المنتج")
    product = st.text_input("", "حقائب جلدية")

budget = st.number_input("الميزانية DZD", 1000, 20000, 5000)

if st.button("🚀 نفّذ", type="primary"):
    goal = f"{command} {product} {budget} DZD"
    Path("goal.txt").write_text(goal)
    
    with st.spinner("BEKO يشتغل..."):
        subprocess.run(["python", "beko-agent-main.py"], shell=True)
    
    if Path("plan.json").exists():
        with open("plan.json") as f:
            st.success("تم الإنجاز! 🎉")
            st.json(json.load(f))

# KPIs
st.header("📊 النتائج الحالية")
col1, col2, col3 = st.columns(3)
col1.metric("ROAS", "2.8x")
col2.metric("TRC", "25%")
col3.metric("CPA", "120 DZD")