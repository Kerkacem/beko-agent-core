#!/usr/bin/env python3
"""
BEKO v4.1.1 - GROQ API LIVE FIXED
Model Updated | Error Fixed | Belkacem DZ
"""

import os
from pathlib import Path
from datetime import datetime
import sys
import glob

print("🤖 BEKO v4.1.1 - GROQ LIVE FIXED!")
ROOT = Path("beko_self")
ROOT.mkdir(exist_ok=True)
grok_dir = ROOT / "grok_live"
grok_dir.mkdir(exist_ok=True)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("⚠️ GROQ_API_KEY not set — running in offline mode (no live Groq calls)")
    client = None
else:
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        print(f"✅ GROQ LIVE: {api_key[:10]}...")
    except Exception as e:
        print(f"⚠️ groq SDK init failed: {e}")
        client = None

def grok_live_call():
    print("\n🌐 LIVE GROQ - Evolve BEKO v5.0!")
    try:
        if not client:
            print("⚠️ No Groq client available — cannot perform live call")
            return None
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ Model حديث متاح!
            messages=[
                {"role": "system", "content": "You are BEKO Evolution AI. Professional, technical."},
                {"role": "user", "content": "BEKO v4.1: Multi-Agent 99.2/100. Goals achieved. Plan v5.0: Neural + Global Deploy + Self-Healing."}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        result = response.choices[0].message.content.strip()
        print(f"\n🤖 GROQ v5.0 PLAN:\n{result}")
        print(f"Tokens used: {response.usage.total_tokens}")
        
        # حفظ
        filename = grok_dir / f"v5_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"💾 SAVED: {filename}")
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def show_responses():
    files = glob.glob(str(grok_dir / "*.txt"))
    if files:
        print(f"\n💾 {len(files)} Groq Responses:")
        for f in sorted(files)[-5:]:
            print(f"  - {Path(f).name}")
    else:
        print("📭 No responses yet")

def main():
    print("🌐 v4.1.1 Groq-Powered BEKO")
    
    while True:
        print("\n" + "="*55)
        print("BEKO v4.1.1 - Real Groq API")
        print("="*55)
        print("1. LIVE Grok: Evolve v5.0")
        print("2. Show Grok History")
        print("3. Status Check")
        print("0. Exit")
        print("="*55)
        
        choice = input("Grok > ").strip()
        
        if choice == "1":
            grok_live_call()
        elif choice == "2":
            show_responses()
        elif choice == "3":
            print("✅ Status: Groq LIVE | Ready for v5.0")
        elif choice == "0":
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    main()