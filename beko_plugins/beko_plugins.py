#!/usr/bin/env python3
"""
BEKO Plugins - Fixed Pylance Errors
"""

import importlib.util
import importlib.machinery
from pathlib import Path
from typing import Optional, Dict, Any

PLUGINS_DIR = Path("beko_plugins")

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.load_plugins()
    
    def load_plugins(self) -> None:
        for plugin_file in PLUGINS_DIR.glob("*.py"):
            if plugin_file.stem != "__init__":
                try:
                    spec = importlib.util.spec_from_file_location(plugin_file.stem, str(plugin_file))
                    if spec is None or spec.loader is None:
                        print(f"❌ Failed to load spec: {plugin_file.stem}")
                        continue
                    
                    module = importlib.util.module_from_spec(spec)
                    spec.loader!.exec_module(module)  # type: ignore
                    self.plugins[plugin_file.stem] = module
                    print(f"✅ Plugin loaded: {plugin_file.stem}")
                except Exception as e:
                    print(f"❌ Plugin error {plugin_file.stem}: {e}")
    
    def run_plugin(self, name: str, *args) -> Optional[Any]:
        if name in self.plugins:
            plugin = self.plugins[name]
            if hasattr(plugin, 'run'):
                return plugin.run(*args)
        print(f"❌ Plugin '{name}' not found")
        return None