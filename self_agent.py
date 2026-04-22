#!/usr/bin/env python3
"""
BEKO SELF-AGENT v1.0 - بناء نفسه + تعلم ذاتي
انسخ + شغل = يبدأ التعلم!
"""

import os
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import sqlite3

print("🤖 BEKO Self-Agent v1.0 - البداية!")
print("📁 إنشاء المجلدات...")

# 1. إعداد المجلدات
ROOT = Path("beko_self")
ROOT.mkdir(exist_ok=True)

for folder in ["skills", "code", "memory", "logs", "tools"]:
    (ROOT / folder).mkdir(exist_ok=True)

DB_PATH = ROOT / "memory" / "agent.db"

print("✅ المجلدات جاهزة!")


# 2. قاعدة البيانات
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c
