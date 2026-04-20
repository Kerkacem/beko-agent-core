import os
import json
import re
from pathlib import Path
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("Set: $env:GROQ_API_KEY='gsk_...'")
    exit(1)

client = Groq(api_key=GROQ_API_KEY)

def clean_response(text):
    # إزالة ```json و ```
    text = re.sub(r'```json|```', '', text)
    text = re.sub(r'```.*```', '', text, flags=re.DOTALL)
    return text.strip()

def load_goal():
    p = Path("goal.txt")
    if p.exists():
        try:
            return p.read_text(errors='ignore').strip()
        except:
            pass
    return "build flask login api"

def main():
    goal = load_goal()
    print("Goal:", goal)
    
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": f"Goal: {goal}\nRespond ONLY with valid JSON: {{\"thought\":\"reason\", \"steps\":[{{\"action\":\"write_file\",\"path\":\"app.py\",\"content\":\"flask code\"}}]}} NO other text."}],
        temperature=0.0
    )
    
    content = clean_response(resp.choices[0].message.content or "{}")
    print("Raw response:", repr(content[:100]))
    
    # جرب parse أو fallback
    try:
        plan = json.loads(content)
    except:
        plan = {
            "thought": "AI returned invalid JSON - using fallback Flask app",
            "steps": [{
                "action": "write_file",
                "path": "app.py",
                "content": '''from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    if username == 'admin' and password == '1234':
        return jsonify({"token": "jwt_token_here", "status": "success"})
    return jsonify({"error": "invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)
'''
            }]
        }
    
    Path("plan.json").write_text(json.dumps(plan, indent=2))
    print("Plan ready:", json.dumps(plan['steps'], indent=2))
    
    # نفّذ مباشرة
    for i, step in enumerate(plan.get('steps', [])):
        if step.get('action') == 'write_file':
            Path(step['path']).write_text(step['content'])
            print(f"Wrote {step['path']}")

if __name__ == "__main__":
    main()