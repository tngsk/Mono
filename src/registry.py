import json
import logging
from pathlib import Path
from typing import Dict, List

from src.constants import COMPONENTS_DIR

logger = logging.getLogger("markdown_converter.registry")

class ComponentRegistry:
    """コンポーネントのメタデータを管理するレジストリクラス"""

    _instance = None
    _components_meta: Dict[str, dict] = {}
    _is_initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ComponentRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_initialized:
            self._load_all_manifests()
            self.__class__._is_initialized = True

    def _load_all_manifests(self):
        """コンポーネントディレクトリを走査し、各マニフェストを読み込む"""
        self._components_meta.clear()

        if not COMPONENTS_DIR.exists() or not COMPONENTS_DIR.is_dir():
            logger.warning(f"Component directory not found: {COMPONENTS_DIR}")
            return

        for component_dir in COMPONENTS_DIR.iterdir():
            if not component_dir.is_dir():
                continue

            manifest_file = component_dir / "manifest.json"
            if manifest_file.exists():
                try:
                    with open(manifest_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        self._components_meta[component_dir.name] = meta
                except Exception as e:
                    logger.error(f"Failed to load manifest for {component_dir.name}: {e}")
            else:
                # Fallback default values if manifest is missing (for backward compatibility during migration)
                self._components_meta[component_dir.name] = {
                    "name": component_dir.name,
                    "interactive": False,
                    "always_include": False,
                    "requires_code_block_highlight": False,
                    "requires_icons": False
                }

    def get_all_components(self) -> List[str]:
        return list(self._components_meta.keys())

    def get_interactive_components(self) -> List[str]:
        return [name for name, meta in self._components_meta.items() if meta.get("interactive", False)]

    def get_always_include_components(self) -> List[str]:
        return [name for name, meta in self._components_meta.items() if meta.get("always_include", False)]

    def get_components_requiring_code_block_highlight(self) -> List[str]:
        return [name for name, meta in self._components_meta.items() if meta.get("requires_code_block_highlight", False)]

    def get_components_requiring_icons(self) -> List[str]:
        return [name for name, meta in self._components_meta.items() if meta.get("requires_icons", False)]

    def get_component_meta(self, component_name: str) -> dict:
        return self._components_meta.get(component_name, {})

# Convenience global functions to access the singleton registry
_registry = ComponentRegistry()

def get_all_components() -> List[str]:
    return _registry.get_all_components()

def get_interactive_components() -> List[str]:
    return _registry.get_interactive_components()

def get_always_include_components() -> List[str]:
    return _registry.get_always_include_components()

def get_components_requiring_code_block_highlight() -> List[str]:
    return _registry.get_components_requiring_code_block_highlight()

def get_components_requiring_icons() -> List[str]:
    return _registry.get_components_requiring_icons()

def get_component_meta(component_name: str) -> dict:
    return _registry.get_component_meta(component_name)
