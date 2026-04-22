#!/usr/bin/env python3
import pytest
import sys

sys.path.insert(0, "..")
from skills.skill_test import TestSkill


def test_generate_real_asserts():
    ts = TestSkill()
    code = """
def hello():
    x = 42
    return x
"""
    path = ts.generate_test(code, "hello")
    with open(path) as f:
        content = f.read()
    assert "ast.parse" not in content  # Generated, not source
    assert "assert" in content
    assert "x" in content or "hello" in content


def test_run_pytest():
    ts = TestSkill()
    result = ts.run_skill({"action": "run"})
    assert "status" in result
