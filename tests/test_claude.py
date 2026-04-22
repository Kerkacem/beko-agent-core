import pytest
from skills.skill_claude import ClaudeSkill
from skills import ClaudeSkill as CS


def test_claude_skill_import():
    assert CS is not None, "ClaudeSkill import failed"


def test_claude_run_skill():
    cs = ClaudeSkill()
    result = cs.run_skill({"action": "chain", "goal": "test"})
    assert result["status"] == "deep chain executed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
