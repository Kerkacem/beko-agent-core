import os
import json
from pathlib import Path

def load_goal():
    goal_file = Path("goal.txt")
    if goal_file.exists():
        text = goal_file.read_text(encoding="utf-8").strip()
        lines = [l for l in text.split("\n") if l.strip()]

        # اول سطر اسم المهارة
        name = lines[0].strip().lower().replace(" ", "-")

        # باقي النص description
        desc = " ".join(lines[1:]) if len(lines) > 1 else "skill auto generated"

        return name, desc
    
    return "default-skill", "auto skill"

def create_skill():
    name, desc = load_goal()

    base = Path(f"./beko-skills/{name}")
    paths = {
        "root": base,
        "skill": base / "SKILL.md",
        "evals": base / "evals" / "evals.json",
        "scripts": base / "scripts",
        "refs": base / "references",
        "assets": base / "assets"
    }

    # folders
    base.mkdir(parents=True, exist_ok=True)
    paths["scripts"].mkdir(parents=True, exist_ok=True)
    paths["refs"].mkdir(parents=True, exist_ok=True)
    paths["assets"].mkdir(parents=True, exist_ok=True)
    paths["evals"].parent.mkdir(parents=True, exist_ok=True)

    skill_md = f"""---
name: {name}
description: {desc}. استعملها كي يكون نفس الطلب
compatibility:
  - Claude Code
  - Claude.ai
---

# {name}

## الهدف
{desc}

## workflow
1. فهم
2. تحليل
3. draft
4. test
5. تحسين

## output
واضح + عملي
"""

    paths["skill"].write_text(skill_md, encoding="utf-8")

    evals_data = {
        "skill_name": name,
        "evals": [
            {"id": 1, "prompt": f"ساعدني ندير {desc}", "expected_output": "نتيجة", "files": []},
            {"id": 2, "prompt": f"مشكلة في {desc}", "expected_output": "حل", "files": []}
        ]
    }

    paths["evals"].write_text(json.dumps(evals_data, indent=2, ensure_ascii=False), encoding="utf-8")

    (paths["scripts"] / "helper.py").write_text("""def run():
    print("ok")

if __name__ == "__main__":
    run()
""", encoding="utf-8")

    print("تم", base)

if __name__ == "__main__":
    create_skill()