#!/usr/bin/env python3
import pytest
import sys

sys.path.insert(0, "..")
from skills.skill_deploy import DeploySkill


def test_deploy_init():
    ds = DeploySkill()
    assert hasattr(ds, "branch_prefix")


def test_run_skill():
    ds = DeploySkill()
    result = ds.run_skill({"action": "commit_push", "msg": "test"})
    assert "status" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
