#!/usr/bin/env python3
"""
BEKO Plugins - Modular Extensions
Load Skills Dynamically
"""

import importlib.util
from pathlib import Path

PLUGINS_DIR = Path("beko_plugins")


class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        for plugin_file in PLUGINS_DIR.glob("*.py"):
            if plugin_file.stem != "__init__":
                try:
                    spec = importlib.util.spec_from_file_location(
                        plugin_file.stem, plugin_file
                    )
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.plugins[plugin_file.stem] = module
                    print(f"✅ Plugin loaded: {plugin_file.stem}")
                except Exception as e:
                    print(f"❌ Plugin error {plugin_file.stem}: {e}")

    def run_plugin(self, name, *args):
        if name in self.plugins:
            plugin = self.plugins[name]
            if hasattr(plugin, "run"):
                return plugin.run(*args)
        print(f"❌ Plugin '{name}' not found")
        return None


# مثال Plugin
if __name__ == "__main__":
    pm = PluginManager()
    pm.run_plugin("meta_ads", "DZD COD")
