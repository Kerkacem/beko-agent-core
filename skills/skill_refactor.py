#!/usr/bin/env python3
"""BEKO Skill #4: Refactor - Auto-clean/rewrite code with black/AST/Groq"""

import ast
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any
from groq import Groq


class RefactorSkill:
    def __init__(self):
        self.client = None
        if os.getenv("GROQ_API_KEY"):
            self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def black_format(self, code: str) -> str:
        """Apply black formatter"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            tmp_path = f.name
        try:
            subprocess.run(["black", tmp_path], capture_output=True, check=True)
            return Path(tmp_path).read_text()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def analyze_ast(self, code: str) -> Dict:
        """AST analysis for issues"""
        try:
            tree = ast.parse(code)
            issues = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module == "torch":
                    issues.append("torch heavy dep")
                if isinstance(node, ast.FunctionDef) and not node.body:
                    issues.append(f"empty def {node.name}")
            return {
                "issues": issues,
                "funcs": len(
                    [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
                ),
            }
        except SyntaxError as e:
            return {"error": str(e)}

    def groq_refactor(self, code: str) -> str:
        """Groq-powered code rewrite"""
        if not self.client:
            return self.black_format(code)
        prompt = f"""Rewrite this Python code to be cleaner, add error handling, remove unused:

```python
{code}
```
Return ONLY the rewritten code."""
        try:
            res = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
            )
            return res.choices[0].message.content.strip("```python").strip("```")
        except:
            return self.black_format(code)

    def run_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        action = params.get("action", "analyze")
        if action == "analyze":
            code = params.get("code", "")
            return self.analyze_ast(code)
        elif action == "format":
            code = params.get("code", "")
            return {"status": "formatted", "code": self.black_format(code)}
        elif action == "refactor":
            code = params.get("code", "")
            return {"status": "refactored", "code": self.groq_refactor(code)}
        return {"error": "action: analyze|format|refactor"}


if __name__ == "__main__":
    rs = RefactorSkill()
    print(
        json.dumps(
            rs.run_skill({"action": "analyze", "code": "def test(): pass"}), indent=2
        )
    )
