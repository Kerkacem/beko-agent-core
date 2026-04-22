#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import json
from skills.skill_memory import MemorySkill


def test_memory_load_save():
    ms = MemorySkill()
    data = {"test": "data"}
    result = ms.run_skill({"action": "save", "data": data})
    assert result["status"] == "saved"

    loaded = ms.run_skill({"action": "load"})
    assert "test" in loaded["kb"]


def test_status_log():
    ms = MemorySkill()
    ms.run_skill({"action": "status", "scanned": 10, "fixed": 2, "health": "70%"})
    with open("logs/hourly_status.json") as f:
        status = json.load(f)
    assert status["files_scanned"] == 10
