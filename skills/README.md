# BEKO Skills - Self-Expansion Modules v1.0

## Priority Order (PHASE 4):
1. **skill_memory.py** - Read/write knowledge_base.json + DB sync
2. skill_search.py - Web search integration
3. skill_test.py - Auto-generate/run pytest
4. skill_refactor.py - Code rewrite analyzer
5. skill_plan.py - Multi-step planner
6. skill_self_heal.py - Advanced error detection/fix
7. skill_deploy.py - Git push automation

Each skill: run_skill(params) → dict result. Importable.

**Usage:** from skills.skill_memory import MemorySkill; ms = MemorySkill(); ms.save({"key": "val"})

