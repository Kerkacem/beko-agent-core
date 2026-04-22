#!/usr/bin/env python3
import pytest
import sys

sys.path.insert(0, "..")
from skills.skill_refactor import RefactorSkill


def test_analyze_ast():
    rs = RefactorSkill()
    code = "def test(): pass"
    result = rs.run_skill({"action": "analyze", "code": code})
    assert "issues" in result
    assert isinstance(result["issues"], list)


def test_black_format():
    rs = RefactorSkill()
    code = 'def test():print("hi")'
    result = rs.run_skill({"action": "format", "code": code})
    assert "def test():" in result["code"]
    assert result["status"] == "formatted"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
