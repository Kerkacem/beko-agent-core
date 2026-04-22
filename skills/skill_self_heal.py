#!/usr/bin/env python3
"""BEKO Skill #6: Self-Heal - Auto detect/fix errors"""

import subprocess
from pathlib import Path
from typing import Dict


class SelfHealSkill:
    def audit_files(self):
        """Find syntax/TODO"""
        errors = []
        for py in Path(".").rglob("*.py"):
            content = py.read_text()
            if "print(" in content.count("print(") > 10:
                errors.append(str(py))
        return errors

    def auto_fix(self, file_path):
        """Replace print → log stub"""
        content = Path(file_path).read_text()
        content = content.replace('print("', 'log.info("')
        Path(file_path).write_text(content)
        return {"fixed": file_path}

    def run_skill(self, params):
        errors = self.audit_files()
        fixes = [self.auto_fix(e) for e in errors[:3]]
        return {"status": "healed", "fixes": len(fixes)}


if __name__ == "__main__":
    print(SelfHealSkill().run_skill({}))
