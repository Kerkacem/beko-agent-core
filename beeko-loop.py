import subprocess
import sys
import os

def run(cmd):
    result = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, cwd=".")
    print(f"--- {cmd[0]} ---")
    print(result.stdout)
    if result.stderr: print(result.stderr)
    if result.returncode != 0:
        print(f"❌ {cmd[0]} failed")
        sys.exit(1)
    return result

if __name__ == "__main__":
    # توليد الخطة
    run(["beko-agent-main.py"])
    
    # التحقق من وجود plan.json
    if not os.path.exists("plan.json"):
        print("❌ plan.json not created!")
        sys.exit(1)
    
    # تنفيذ الخطة  
    run(["beeko-runner.py"])
    
    print("✅ BEKO Loop completed!")