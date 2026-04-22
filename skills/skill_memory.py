#!/usr/bin/env python3
"""BEKO Skill #1: Memory - PHASE 4 Self-Expansion"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class MemorySkill:
    def __init__(self, base_path: str = "."):
        self.kb_path = Path(base_path) / "memory/knowledge_base.json"
        self.status_path = Path(base_path) / "logs/hourly_status.json"
        self.db_path = Path(base_path) / "beko_fixes.db"  # Reuse existing

    def load_kb(self) -> Dict[str, Any]:
        """Load knowledge base"""
        if self.kb_path.exists():
            with open(self.kb_path, "r", encoding="utf-8") as f:
                return json.loads(f.read())
        return {}

    def save_kb(self, data: Dict[str, Any]):
        """Save/update knowledge base"""
        kb = self.load_kb()
        kb.update(data)
        kb["last_updated"] = datetime.now().isoformat()
        self.kb_path.parent.mkdir(exist_ok=True)
        with open(self.kb_path, "w", encoding="utf-8") as f:
            json.dump(kb, f, indent=2, ensure_ascii=False)
        return kb

    def log_status(self, files_scanned: int, errors_fixed: int, health: str):
        """Update hourly status (PHASE 6)"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "files_scanned": files_scanned,
            "errors_fixed": errors_fixed,
            "health": health,
        }
        self.status_path.parent.mkdir(exist_ok=True)
        with open(self.status_path, "w") as f:
            json.dump(status, f, indent=2)

    def run_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Skill interface"""
        action = params.get("action", "load")
        if action == "save":
            return {"status": "saved", "data": self.save_kb(params.get("data", {}))}
        elif action == "load":
            return {"status": "loaded", "kb": self.load_kb()}
        elif action == "status":
            self.log_status(
                params.get("scanned", 0),
                params.get("fixed", 0),
                params.get("health", "50%"),
            )
            return {"status": "logged"}
        return {"error": "unknown action"}


# Test
if __name__ == "__main__":
    ms = MemorySkill()
    print(ms.run_skill({"action": "load"}))
