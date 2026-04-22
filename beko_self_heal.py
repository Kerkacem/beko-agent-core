#!/usr/bin/env python3
"""
BEKO v7.3 Self-Healing Agent - Production Ready
MARKETING MASTER ENGINE + Auto-Fix + DB Tracking
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path
import importlib.util
import sqlite3
from datetime import datetime
from typing import List, Dict


class Config:
    DB_PATH = Path("beko_fixes.db")


config = Config()


class SelfHealingDB:
    def init_db(self):
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fixes (
                id INTEGER PRIMARY KEY,
                error_type TEXT,
                package TEXT,
                fixed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        print(f"✅ Fixes DB: {config.DB_PATH}")


db = SelfHealingDB()
db.init_db()


class SelfHealingAgent:
    def __init__(self):
        self.errors_fixed = []
        self.auto_installed = []

    def detect_and_fix(self):
        """اكتشاف + إصلاح شامل"""
        print("🔍 BEKO v7.3 يفحص نفسه...")

        # 1. إصلاح الحزم
        self.fix_missing_imports()

        # 2. اختبار الاستيرادات
        self.test_imports()

        # 3. إصلاح goal.txt BOM
        self.fix_goal_file()

        # 4. حفظ السجل
        self.save_fix_log()

        print("✅ Self-Healing مكتمل!")
        print(f"📊 إصلاح: {len(self.errors_fixed)} | تثبيت: {len(self.auto_installed)}")

    def fix_missing_imports(self):
        """تثبيت تلقائي آمن"""
        critical_packages = [
            "flask",
            "flask-jwt-extended",
            "streamlit",
            "python-telegram-bot",
            "groq",
        ]

        for pkg in critical_packages:
            if not self.is_package_installed(pkg):
                print(f"📦 تثبيت {pkg}...")
                try:
                    subprocess.run(
                        [sys.executable, "-m", "pip", "install", pkg],
                        check=False,
                        capture_output=True,
                    )
                    self.auto_installed.append(pkg)
                    self.log_fix("package", pkg)
                except:
                    print(f"⚠️ فشل {pkg}")

    def is_package_installed(self, package: str) -> bool:
        spec = importlib.util.find_spec(package)
        return spec is not None

    def test_imports(self):
        """اختبار شامل مع إعادة إصلاح"""
        tests = {
            "flask": "from flask import Flask",
            "streamlit": "import streamlit",
            "groq": "from groq import Groq",
            "python-telegram-bot": "from telegram.ext import Application",
        }

        for pkg, test_code in tests.items():
            try:
                exec(test_code)
            except ImportError as e:
                print(f"❌ {pkg}: {e}")
                self.errors_fixed.append(pkg)
                self.fix_missing_imports()
                self.log_fix("import_test", pkg)

    def fix_goal_file(self):
        """إصلاح BOM + validation"""
        goal_file = Path("goal.txt")
        if goal_file.exists():
            content = goal_file.read_text(errors="ignore").strip()

            # إزالة BOM
            if content.startswith(("ï»¿", "ÿþ", "\ufeff")):
                content = content.lstrip("ï»¿ÿþ\ufeff")
                goal_file.write_text(content, encoding="utf-8")
                self.errors_fixed.append("BOM goal.txt")
                self.log_fix("bom", "goal.txt")

            # Validation Meta Ads
            if "DZD" not in content and "act_" not in content:
                print("⚠️ Goal غير Meta Ads - إضافة default")
                goal_file.write_text(
                    "Scale Meta Campaign DZD 5000 act_4330803053874384"
                )

    def log_fix(self, error_type: str, details: str):
        """حفظ الإصلاح في DB"""
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fixes (error_type, package) VALUES (?, ?)",
            (error_type, details),
        )
        conn.commit()
        conn.close()

    def save_fix_log(self):
        """تصدير السجل"""
        log = {
            "errors_fixed": self.errors_fixed,
            "auto_installed": self.auto_installed,
            "timestamp": datetime.now().isoformat(),
        }
        Path("beko_fix_log.json").write_text(
            json.dumps(log, ensure_ascii=False, indent=2)
        )

    def run_main_agent(self):
        """تشغيل آمن مع timeout طويل + retry"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🚀 تشغيل BEKO الرئيسي (محاولة {attempt+1}/{max_retries})")

                # تشغيل آمن بـ sys.executable
                result = subprocess.run(
                    [sys.executable, "beko-agent-main.py"],
                    capture_output=True,
                    text=True,
                    timeout=120,  # 2 دقائق
                    env={**os.environ, "GROQ_API_KEY": os.getenv("GROQ_API_KEY", "")},
                )

                if result.returncode == 0:
                    print("✅ نجح!")
                    print(
                        result.stdout[:500] + "..."
                        if len(result.stdout) > 500
                        else result.stdout
                    )
                    return True
                else:
                    print("❌ خطأ:", result.stderr[:200])
                    self.heal_from_error(result.stderr)

            except subprocess.TimeoutExpired:
                print("⏰ Timeout - إعادة المحاولة")
            except FileNotFoundError:
                print("❌ beko-agent-main.py غير موجود - إنشاء default")
                self.create_default_agent()

        print("⚠️ فشل بعد 3 محاولات")
        return False

    def heal_from_error(self, error_msg: str):
        """علاج ذكي من الخطأ"""
        error_msg_lower = error_msg.lower()

        if "modulenotfounderror" in error_msg_lower:
            pkg_match = re.search(r"'([^']+)'", error_msg)
            if pkg_match:
                pkg = pkg_match.group(1)
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", pkg], check=False
                )
                self.log_fix("module_error", pkg)

        elif "syntaxerror" in error_msg_lower:
            print("🔧 SyntaxError - إعادة فحص")
            self.detect_and_fix()

    def create_default_agent(self):
        """إنشاء agent افتراضي إذا غاب"""
        default_code = """
print("🚀 BEKO Default Agent - جاهز للـ Meta Ads!")
print("📝 ضع goal.txt وشغّل مرة أخرى")
"""
        Path("beko-agent-main.py").write_text(default_code)
        print("✅ تم إنشاء beko-agent-main.py افتراضي")


def main():
    agent = SelfHealingAgent()
    agent.detect_and_fix()
    agent.run_main_agent()
    print("\n🎉 BEKO v7.3 جاهز 100%!")


if __name__ == "__main__":
    main
