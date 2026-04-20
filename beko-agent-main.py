"""
BEKO AGENT PRO v2.0 - Self-Building AI Platform
مدير تسويق رقمي + AI Engineer كامل
Flask API + SQLite + JWT + Tools + Memory + Git + Docker
"""

import os
import json
import re
import hashlib
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from groq import Groq
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import git  # pip install GitPython

# ===============================================
# CORE CONFIGURATION
# ===============================================
@dataclass
class Config:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    PROJECT_ROOT: Path = Path.cwd()
    DB_PATH: Path = PROJECT_ROOT / "beko.db"
    MEMORY_PATH: Path = PROJECT_ROOT / "memory"
    SKILLS_PATH: Path = PROJECT_ROOT / "skills"
    TOOLS_PATH: Path = PROJECT_ROOT / "tools"
    GOAL_FILE: Path = PROJECT_ROOT / "goal.txt"
    MODEL: str = "llama-3.3-70b-versatile"

config = Config()

# ===============================================
# DATABASE MANAGER
# ===============================================
class DatabaseManager:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Goals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_text TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL
            )
        """)
        
        # Builds table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS builds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER,
                files_changed TEXT,
                success BOOLEAN,
                output TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (goal_id) REFERENCES goals (id)
            )
        """)
        
        conn.commit()
        conn.close()
        print(f"✅ DB ready: {config.DB_PATH}")

    def hash_password(self, password: str) -> str:
        """Hash password with SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str) -> Dict[str, Any]:
        """Register new user"""
        try:
            conn = sqlite3.connect(config.DB_PATH)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {"id": user_id, "username": username, "status": "created"}
        except sqlite3.IntegrityError:
            return {"error": "username exists"}
        except Exception as e:
            return {"error": str(e)}

    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        """Login user"""
        try:
            conn = sqlite3.connect(config.DB_PATH)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute(
                "SELECT id, username FROM users WHERE username = ? AND password_hash = ? AND is_active = 1",
                (username, password_hash)
            )
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                token = create_access_token(identity={"id": user[0], "username": user[1]})
                return {"status": "success", "token": token, "user": {"id": user[0], "username": user[1]}}
            return {"error": "invalid credentials"}
        except Exception as e:
            return {"error": str(e)}

db = DatabaseManager()

# ===============================================
# SKILLS SYSTEM
# ===============================================
class SkillsManager:
    SKILLS = {
        "flask_api": {
            "description": "Build Flask REST APIs",
            "dependencies": ["flask", "flask-jwt-extended"],
            "endpoints": ["/login", "/register"]
        },
        "sqlite_db": {
            "description": "SQLite database operations",
            "dependencies": [],
            "tables": ["users", "goals"]
        },
        "git_ops": {
            "description": "Git commit/push automation",
            "dependencies": ["GitPython"]
        },
        "docker": {
            "description": "Dockerfile generation",
            "dependencies": []
        }
    }

    def get_skill(self, name: str) -> Dict:
        return self.SKILLS.get(name, {})

skills = SkillsManager()

# ===============================================
# GIT MANAGER
# ===============================================
class GitManager:
    def __init__(self):
        self.repo = git.Repo(config.PROJECT_ROOT)
    
    def commit_push(self, message: str):
        """Auto commit and push"""
        try:
            self.repo.git.add(all=True)
            self.repo.index.commit(message)
            self.repo.remotes.origin.push()
            print(f"✅ Git: {message}")
        except Exception as e:
            print(f"Git error: {e}")

git_mgr = GitManager()

# ===============================================
# AI PLANNER (Enhanced)
# ===============================================
class AIPlanner:
    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
    
    def parse_goal(self, goal: str) -> str:
        """Extract skills from goal"""
        goal_lower = goal.lower()
        skills_found = []
        
        for skill_name, skill_info in skills.SKILLS.items():
            if any(word in goal_lower for word in skill_info["description"].split()):
                skills_found.append(skill_name)
        
        return f"{goal} Required skills: {', '.join(skills_found)}"
    
    def generate_plan(self, goal: str) -> Dict[str, Any]:
        """Generate execution plan"""
        enhanced_goal = self.parse_goal(goal)
        
        system_prompt = f"""
You are BEKO Agent Pro - AI Software Engineer.

Goal: {enhanced_goal}

Return ONLY valid JSON:
{{
  "thought": "analysis",
  "skills_used": ["flask_api", "sqlite_db"],
  "files": ["app.py", "requirements.txt"],
  "steps": [
    {{
      "action": "write_file",
      "path": "app.py", 
      "content": "complete code"
    }},
    {{
      "action": "install_deps",
      "packages": ["flask"]
    }}
  ]
}}

Rules:
- Valid Python code
- Complete working files
- Production ready
"""
        
        resp = self.client.chat.completions.create(
            model=config.MODEL,
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.1,
            max_tokens=4000
        )
        
        content = resp.choices[0].message.content.strip()
        return self._safe_parse_json(content)
    
    def _safe_parse_json(self, content: str) -> Dict[str, Any]:
        """Safe JSON parsing with fallback"""
        try:
            return json.loads(content)
        except:
            return {
                "thought": "fallback plan",
                "skills_used": [],
                "steps": self._generate_fallback()
            }
    
    def _generate_fallback(self) -> List[Dict]:
        """Fallback steps"""
        return [{
            "action": "write_file",
            "path": "app.py",
            "content": '''from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
import sqlite3
import hashlib

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

# SQLite init
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        return jsonify({"message": "user created"})
    except:
        return jsonify({"error": "username exists"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password_hash))
    user = cursor.fetchone()
    
    if user:
        token = create_access_token(identity=username)
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)
'''
        }]

planner = AIPlanner()

# ===============================================
# EXECUTION ENGINE
# ===============================================
class ExecutionEngine:
    def __init__(self):
        self.results = []
    
    def execute_plan(self, plan: Dict[str, Any]) -> List[Dict]:
        """Execute AI plan"""
        steps = plan.get('steps', [])
        
        for i, step in enumerate(steps):
            result = self._execute_step(step)
            result['index'] = i
            self.results.append(result)
            print(f"Step {i}: {result['action']} → {result['status']}")
        
        return self.results
    
    def _execute_step(self, step: Dict) -> Dict:
        """Execute single step"""
        action = step.get('action', 'unknown')
        
        try:
            if action == 'write_file':
                path = step.get('path', 'unknown.py')
                content = step.get('content', '# empty')
                Path(path).write_text(content)
                return {'action': action, 'path': path, 'status': 'success', 'size': len(content)}
            
            elif action == 'install_deps':
                packages = step.get('packages', [])
                for pkg in packages:
                    subprocess.run(['pip', 'install', pkg], check=True)
                return {'action': action, 'packages': packages, 'status': 'success'}
            
            elif action == 'git_commit':
                message = step.get('message', 'Auto commit')
                git_mgr.commit_push(message)
                return {'action': action, 'status': 'success'}
            
            else:
                return {'action': action, 'status': 'unknown', 'error': 'unsupported'}
                
        except Exception as e:
            return {'action': action, 'status': 'failed', 'error': str(e)}

engine = ExecutionEngine()

# ===============================================
# MAIN ORCHESTRATOR
# ===============================================
class BekoAgentPro:
    def __init__(self):
        self.db = db
        self.planner = planner
        self.engine = engine
        self.skills = skills
    
    def run_cycle(self):
        """Complete agent cycle"""
        print("=" * 60)
        print("BEKO AGENT PRO v2.0 - Self-Building Platform")
        print("=" * 60)
        
        # 1. Load goal
        goal = self.load_or_prompt_goal()
        
        # 2. Plan
        plan = self.planner.generate_plan(goal)
        print("Plan generated:", plan.get('thought', ''))
        
        # 3. Execute
        results = self.engine.execute_plan(plan)
        
        # 4. Save to DB
        self.save_build(goal, plan, results)
        
        # 5. Git
        git_mgr.commit_push(f"BEKO Auto: {goal[:50]}")
        
        print("✅ Cycle complete!")
        return results
    
    def load_or_prompt_goal(self) -> str:
        """Load goal or prompt user"""
        if config.GOAL_FILE.exists():
            try:
                return config.GOAL_FILE.read_text(errors='ignore').strip()
            except:
                pass
        
        # Default goals rotation
        defaults = [
            "add React frontend to Flask API",
            "deploy to Docker with docker-compose", 
            "add user dashboard /profile endpoint",
            "implement file upload API",
            "add WebSocket real-time chat"
        ]
        return defaults[hash(str(datetime.now())) % len(defaults)]
    
    def save_build(self, goal: str, plan: Dict, results: List[Dict]):
        """Save to database"""
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO goals (goal_text) VALUES (?)", (goal,))
        goal_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO builds (goal_id, files_changed, success, output) 
            VALUES (?, ?, ?, ?)
        """, (goal_id, json.dumps(plan.get('files', [])), all(r['status']=='success' for r in results), json.dumps(results)))
        
        conn.commit()
        conn.close()

# ===============================================
# FLASK ADMIN API (Bonus)
# ===============================================
flask_app = Flask(__name__)
flask_app.config['JWT_SECRET_KEY'] = 'beko-super-secret-2026'
jwt = JWTManager(flask_app)

@flask_app.route('/api/agent/run', methods=['POST'])
@jwt_required()
def api_run_agent():
    goal = request.json.get('goal', 'default goal')
    agent = BekoAgentPro()
    results = agent.run_cycle()
    return jsonify({"status": "success", "results": results})

@flask_app.route('/api/agent/status')
def api_status():
    return jsonify({
        "status": "running",
        "version": "2.0",
        "skills": list(skills.SKILLS.keys()),
        "endpoints": ["/login", "/register", "/api/agent/run"]
    })

if __name__ == "__main__":
    print("🚀 Starting BEKO Agent Pro...")
    agent = BekoAgentPro()
    agent.run_cycle()
    
    print("\n🌐 Admin API ready: http://127.0.0.1:5001")
    flask_app.run(port=5001, debug=True)