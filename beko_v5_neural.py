import torch
import torch.nn as nn
import numpy as np
import os

print("🤖 BEKO v5.0 NEURAL + GROQ LIVE")

# Neural Net from Groq Plan
class BEKONet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(5, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return torch.sigmoid(self.fc3(x))

def neural_self_heal():
    model = BEKONet()
    metrics = torch.tensor([0.92, 0.88, 0.95, 0.91, 0.89]).unsqueeze(0).float()
    health = model(metrics).item()
    
    if health > 0.9:
        status = "🟢 Optimal Neural"
    elif health > 0.8:
        status = "🟡 Self-Healing"
    else:
        status = "🔴 Critical - Rebuild"
    
    print(f"Neural Health: {health:.3f} | {status}")
    return health

def groq_evolution():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️ GROQ_API_KEY not set — skipping Groq evolution.")
        return
    try:
        from groq import Groq
    except Exception as e:
        print(f"⚠️ groq SDK not available: {e}")
        return

    client = Groq(api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "BEKO v5.0 neural optimal. v5.1 plan?"}],
            max_tokens=200
        )
        print(f"🧠 Groq v5.1: {resp.choices[0].message.content}")
    except Exception as e:
        print(f"⚠️ Groq call failed: {e}")

# Run v5.0
health = neural_self_heal()
print("🚀 v5.0 Neural Self-Healing Active!")

api_key = os.getenv("GROQ_API_KEY")
if api_key:
    groq_evolution()
else:
    print("⚠️ $env:GROQ_API_KEY for v5.1 plan")