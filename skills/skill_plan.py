#!/usr/bin/env python3
"""BEKO Skill #5: Plan - Multi-step planner"""

from groq import Groq
import json
from pathlib import Path


class PlanSkill:
    def generate_plan(self, goal):
        client = Groq()
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Generate JSON plan: {'steps': [{'action': 'str', 'file': 'str', 'desc': 'str'}]}",
                },
                {"role": "user", "content": goal},
            ],
        )
        return json.loads(resp.choices[0].message.content)

    def run_skill(self, params):
        plan = self.generate_plan(params.get("goal", "improve agent"))
        Path("current_plan.json").write_text(json.dumps(plan))
        return {"status": "planned", "steps": len(plan.get("steps", []))}


if __name__ == "__main__":
    print(PlanSkill().run_skill({}))
