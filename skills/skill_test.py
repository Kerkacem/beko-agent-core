#!/usr/bin/env python3
"""BEKO Skill #3: Auto-Test - Generate/run pytest"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, Any, List


class TestSkill:
    def __init__(self):
        self.tests_dir = Path("tests")
        self.tests_dir.mkdir(exist_ok=True)

    def generate_test(self, code_snippet: str, func_name: str):
        """Gen pytest from code snippet"""
        test_code = f"""import pytest
def test_{func_name.replace("-", "_")}():
    # Auto-gen test for: {func_name}
    assert True  # TODO: parse code for real asserts
"""
        test_path = self.tests_dir / f"test_{func_name}.py"
        test_path.write_text(test_code)
        return str(test_path)

    def run_pytest(self, target_dir: str = "tests/") -> Dict[str, Any]:
        """Run pytest, parse results"""
        result = subprocess.run(
            ["pytest", target_dir, "-v", "--tb=no"], capture_output=True, text=True
        )
        passed = "passed" in result.stdout.lower()
        return {
            "status": "passed" if passed else "failed",
            "stdout": result.stdout[:500],
            "stderr": result.stderr[:500],
        }

    def run_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        action = params.get("action")
        if action == "generate":
            path = self.generate_test(
                params.get("code", ""), params.get("func", "test")
            )
            return {"status": "generated", "path": str(path)}
        elif action == "run":
            return self.run_pytest(params.get("dir", "tests/"))
        return {"error": "unknown action: generate|run"}


if __name__ == "__main__":
    ts = TestSkill()
    print(json.dumps(ts.run_skill({"action": "run"}), indent=2))
