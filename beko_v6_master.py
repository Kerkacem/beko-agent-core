#!/usr/bin/env python3
"""
BEKO v6.0 Master - Skills + Plugins + Deep Think
Production Framework | Belkacem DZ
"""

from beko_v6_skills import BEKOSkills
from beko_plugins import PluginManager

print("🤖 BEKO v6.0 MASTER AGENT")
print("Skills + Plugins + Deep Thinking")

skills = BEKOSkills()
plugins = PluginManager()

while True:
    cmd = input("\nBEKO v6.0> ").strip()
    
    if cmd.lower() == "skills":
        skills.list_skills()
    elif cmd.lower() == "plugins":
        print("Plugins:", list(plugins.plugins.keys()))
    elif cmd.startswith("skill "):
        skill = cmd.split(" ", 1)[1]
        skills.activate_skill(skill)
    elif cmd.startswith("plugin "):
        parts = cmd.split(" ", 2)
        plugins.run_plugin(parts[1], parts[2] if len(parts) > 2 else "")
    elif cmd.lower() == "quit":
        break
    else:
        print("Commands: skills | plugins | skill <name> | plugin <name> [args] | quit")