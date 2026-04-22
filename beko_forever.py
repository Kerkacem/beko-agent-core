#!/usr/bin/env python3
import os
import subprocess
import time
import sys

# os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
SCRIPT = "beko_production_v5.py"

print("🤖 BEKO FOREVER v4.3")
print("Ctrl+C = Stop | Auto-Restart")

cycle = 0
while True:
    cycle += 1
    print(f"\n[{time.strftime('%H:%M:%S')}] Cycle #{cycle}")
    try:
        result = subprocess.run(
            [sys.executable, SCRIPT], capture_output=False, timeout=280
        )
        print(f"✓ Cycle OK | Exit: {result.returncode}")
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout - Restart")
    except Exception as e:
        print(f"❌ Error: {e} - Restart")

    print("⏳ 30s → Next Cycle...")
    time.sleep(30)
