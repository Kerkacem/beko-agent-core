import os
import json
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("❌ لم يتم العثور على متغير البيئة GROQ_API_KEY")
    print("رجاءً ضع API Key الخاص بـ Groq في متغير البيئة ثم أعد التشغيل.")
    raise SystemExit(1)

groq_client = Groq(api_key=GROQ_API_KEY)

RUNNER_URL = "http://localhost:8002/execute"

SYSTEM_PROMPT = """
You are BEKO Agent, an autonomous coding agent.
You control a project in D:/beko-agent-core through a runner API.

You can ONLY act by returning a JSON object with a 'steps' array.
Each step must be ONE of the following shapes:

1) Write a file:
   {
     "action": "write_file",
     "path": "D:/beko-agent-core/relative/or/absolute/path",
     "content": "full file contents as text"
   }

2) Read a file:
   {
     "action": "read_file",
     "path": "D:/beko-agent-core/relative/or/absolute/path"
   }

3) Run a command:
   {
     "action": "run_command",
     "command": "python | pytest | node | npm | git",
     "args": ["arg1", "arg2", "..."]
   }

Important rules:
- Paths must stay INSIDE D:/beko-agent-core.
- For run_command:
  - Only use allowed commands: python, pytest, node, npm, git.
  - Assume the working directory is D:/beko-agent-core.
  - Start with simple, low-risk commands.

Response format:
- Always respond with PURE JSON, no explanations, no markdown, no fences.
- JSON shape:
  {
    "thought": "short reasoning in English",
    "steps": [ ... ]
  }
"""

def _strip_markdown_fence(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        first_nl = t.find("\n")
        if first_nl != -1:
            t = t[first_nl + 1 :]
        if t.endswith("```"):
            t = t[:-3].strip()
    return t

def call_llm(goal: str) -> dict:
    chat_completion = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Goal:\n{goal}"},
        ],
        temperature=0.2,
        max_completion_tokens=2048,
    )

    content = chat_completion.choices[0].message.content
    if content is None:
        raise RuntimeError("Groq returned no content in message.content")

    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )

    content_clean = _strip_markdown_fence(content)

    try:
        return json.loads(content_clean)
    except json.JSONDecodeError:
        print("❌ الموديل لم يرجع JSON صالح:")
        print(content)
        raise

def main():
    print("=== BEKO Agent (Groq) ===")

    goal_file = "goal.txt"
    if os.path.exists(goal_file):
        with open(goal_file, "r", encoding="utf-8") as f:
            goal = f.read().strip()
        print(f"سيتم استخدام الهدف من {goal_file}")
    else:
        goal = input("اكتب الهدف العام:\n> ")

    plan = call_llm(goal)
    print("Thought:", plan.get("thought"))
    steps = plan.get("steps", [])
    print(f"Agent اقترح {len(steps)} خطوة، سيتم تنفيذها الآن...")
    print(json.dumps({"thought": plan.get("thought"), "steps": steps}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()