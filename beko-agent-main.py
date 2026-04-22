#!/usr/bin/env python3
import os
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Any
from groq import Groq

# Flask (اختياري)
FLASK_AVAILABLE = False
try:
    from flask import Flask, request, jsonify
    from flask_jwt_extended import JWTManager, jwt_required
    FLASK_AVAILABLE = True
except ImportError:
    pass

# CONFIG DZD Ecom
class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PROJECT_ROOT = Path.cwd()
    DB_PATH = PROJECT_ROOT / "beko_v6.db"
    GOAL_FILE = PROJECT_ROOT / "goal.txt"
    MODEL = "llama-3.3-70b-versatile"
    MAX_STEPS = 10

config = Config()
if not config.GROQ_API_KEY:
    print("🚨 $env:GROQ_API_KEY='gsk_...'")
    exit(1)

client = Groq(api_key=config.GROQ_API_KEY)

# DB
class Database:
    def __init__(self):
        conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY,
            name TEXT,
            goal TEXT,
            created TEXT)""")
        conn.commit()
        conn.close()

db = Database()

# JSON Safe
def safe_json(raw: str) -> Dict[str, Any]:
    raw = raw.strip().removeprefix('```json').removesuffix('```')
    try:
        return json.loads(raw)
    except:
        return {
            "thought": "JSON fallback - BEKO safe mode",
            "steps": [{
                "action": "write_file",
                "path": "status.py",
                "content": 'print("BEKO v6.1 OK - DZD Ready")'
            }]
        }

# Goal Loader
def load_goal() -> Dict[str, str]:
    if not config.GOAL_FILE.exists():
        return {"name": "default-skill", "goal": "Build DZD Ecom skill", "output": "SKILL.md + evals"}
    
    data = {}
    try:
        with open(config.GOAL_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    k, v = line.split(':', 1)
                    data[k.strip().lower()] = v.strip()
    except:
        pass
    return {
        "name": data.get("name", "auto-skill"),
        "goal": data.get("goal", ""),
        "output": data.get("output", "")
    }

# SYSTEM PROMPT محسن
SYSTEM_PROMPT = """
BEKO v6.1 DZD Ecom Agent.

RETURN ONLY VALID JSON:

{
  "thought": "short reasoning (Arabic/English)",
  "steps": [
    {
      "action": "write_file",
      "path": "SKILL.md",
      "content": "complete markdown skill"
    },
    {
      "action": "write_file", 
      "path": "evals/evals.json",
      "content": "JSON evals"
    }
  ]
}

Rules:
- DZD currency
- COD 20-40% returns  
- Meta Ads + TRC Protocol
- Clean code, no emoji
"""

def generate_plan(goal: str) -> Dict[str, Any]:
    try:
        res = client.chat.completions.create(
            model=config.MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": goal}
            ],
            temperature=0.1,
            max_tokens=4096
        )
        return safe_json(res.choices[0].message.content)
    except Exception as e:
        print(f"Groq error: {e}")
        return safe_json("API fallback")

# Engine
class Engine:
    def execute(self, plan: Dict[str, Any]) -> List[Dict[str, str]]:
        results = []
        steps = plan.get("steps", [])[:config.MAX_STEPS]
        for step in steps:
            result = self._run_step(step)
            results.append(result)
            print(f"✅ {result['action']}: {result['path']}")
        return results
    
    def _run_step(self, step: Dict[str, Any]) -> Dict[str, str]:
        action = step.get("action", "unknown")
        try:
            if action == "write_file":
                path = step.get("path", "output.txt")
                content = step.get("content", "# BEKO output")
                p = Path(path)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content, encoding="utf-8")
                return {"action": action, "path": str(p), "status": "success", "size": len(content)}
            elif action == "delete_file":
                p = Path(step.get("path", ""))
                if p.exists(): p.unlink()
                return {"action": action, "status": "deleted"}
            return {"action": action, "status": "skipped"}
        except Exception as e:
            return {"action": action, "status": "error", "error": str(e)}

# Flask API
if FLASK_AVAILABLE:
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'beko-v6.1-DZD-secret'
    
    @app.route('/status')
    def status():
        return jsonify({"version": "6.1", "status": "ready", "files": len(list(config.PROJECT_ROOT.glob("*")))})
    
    @app.route('/run', methods=['POST'])
    def api_run():
        goal = request.json.get('goal', 'test')
        g = load_goal()
        plan = generate_plan(f"{g['name']}: {goal}")
        results = Engine().execute(plan)
        return jsonify({"plan": plan, "results": results})

# MAIN
def main():
    print("🔥 BEKO Agent v6.1 - DZD Ecom Production")
    g = load_goal()
    print(f"📋 Goal: {g['name']} | {g['goal'][:50]}...")
    
    goal_prompt = f"""
    Name: {g['name']}
    Goal: {g['goal']}
    Output: {g['output']}
    
    Create COMPLETE skill system:
    - SKILL.md (Claude format)
    - evals/evals.json (3 test cases)
    - scripts/meta-ads.py (helper)
    """
    
    plan = generate_plan(goal_prompt)
    
    # Save Plan
    Path("plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Execute
    results = Engine().execute(plan)
    
    # Save Results
    Path("results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"✅ COMPLETE! {len([r for r in results if r['status']=='success'])} files")
    print("📄 plan.json + results.json")
    
    # API
    if FLASK_AVAILABLE:
        print("🌐 API: http://localhost:5000/status")
        app.run(port=5000, debug=False)

if __name__ == "__main__":
    main()