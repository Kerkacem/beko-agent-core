#!/usr/bin/env python3
"""
BEKO v4.2 - Windows Service + Groq LIVE
Persistent | Background | Belkacem DZ
"""

import os
import time
from groq import Groq
from pathlib import Path
import threading
import sys

ROOT = Path("beko_windows")
ROOT.mkdir(exist_ok=True)


class WindowsBEKO:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.running = True
        print("🤖 BEKO Windows Service v4.2")
        if self.client:
            print("✅ Groq Ready")
        else:
            print("⚠️ Set $env:GROQ_API_KEY")

    def grok_loop(self):
        while self.running:
            try:
                if self.client:
                    resp = self.client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role": "user", "content": "Status check BEKO."}],
                        max_tokens=100,
                    )
                    print(
                        f"[{time.strftime('%H:%M')}] Grok: {resp.choices[0].message.content[:50]}..."
                    )
            except:
                pass
            time.sleep(60)  # كل دقيقة

    def start_service(self):
        # Background Grok
        grok_thread = threading.Thread(target=self.grok_loop, daemon=True)
        grok_thread.start()
        print("🚀 Windows Service Running (Ctrl+C to stop)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
            print("🛑 Service Stopped")


if __name__ == "__main__":
    beko = WindowsBEKO()
    beko.start_service()
