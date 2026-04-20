import json
from pathlib import Path
import shutil

ROOT = Path.cwd().resolve()

def safe_path(path: str) -> Path:
    p = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    if ROOT not in p.parents and p != ROOT:
        raise ValueError(f"Path outside project root: {path}")
    return p

def read_file(path: str) -> str:
    return safe_path(path).read_text(encoding="utf-8")

def write_file(path: str, content: str) -> None:
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def append_file(path: str, content: str) -> None:
    p = safe_path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(content)

def copy_file(src: str, dst: str) -> None:
    s = safe_path(src)
    d = safe_path(dst)
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(s, d)

def make_dir(path: str) -> None:
    safe_path(path).mkdir(parents=True, exist_ok=True)

def list_dir(path: str = "."):
    return [x.name for x in sorted(safe_path(path).iterdir())]

def run_steps(steps):
    results = []
    for i, step in enumerate(steps):
        action = step.get("action")
        try:
            if action == "write_file":
                write_file(step["path"], step["content"])
                results.append({"index": i, "ok": True, "action": action})
            elif action == "append_file":
                append_file(step["path"], step["content"])
                results.append({"index": i, "ok": True, "action": action})
            elif action == "copy_file":
                copy_file(step["src"], step["dst"])
                results.append({"index": i, "ok": True, "action": action})
            elif action == "mkdir":
                make_dir(step["path"])
                results.append({"index": i, "ok": True, "action": action})
            elif action == "read_file":
                results.append({"index": i, "ok": True, "action": action, "content": read_file(step["path"])})
            elif action == "list_dir":
                results.append({"index": i, "ok": True, "action": action, "items": list_dir(step.get("path", "."))})
            else:
                results.append({"index": i, "ok": False, "action": action, "error": "Unknown action"})
        except Exception as e:
            results.append({"index": i, "ok": False, "action": action, "error": str(e)})
    return results

def main():
    p = Path("plan.json")
    if not p.exists() or not p.read_text(encoding="utf-8").strip():
        raise SystemExit("plan.json is missing or empty")

    data = json.loads(p.read_text(encoding="utf-8"))
    steps = data.get("steps", [])
    results = run_steps(steps)
    Path("run-results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()