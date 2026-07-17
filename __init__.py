"""
Module registry.
Each feature/capability of Sentinel is a Module subclass.

Quick-start:
    1. Create a file in this package, e.g. sentinel/modules/monitor.py
    2. Define a class that inherits from BaseModule and implements run().
    3. Register it in sentinel/core/system.py → _load_modules().
"""

from __future__ import annotations

from typing import List


class BaseModule:
    """All Sentinel modules inherit from this class."""

    name: str = "unnamed"

    def run(self) -> None:
        raise NotImplementedError(f"Module '{self.name}' must implement run()")

    def __repr__(self) -> str:
        return f"<Module: {self.name}>"


class ModuleRegistry:
    """Keeps track of every loaded module."""

    def __init__(self) -> None:
        self._modules: List[BaseModule] = []

    def register(self, module: BaseModule) -> None:
        self._modules.append(module)
        print(f"  [+] Module loaded: {module.name}")

    def run_all(self) -> None:
        for module in self._modules:
            module.run()

    def __len__(self) -> int:
        return len(self._modules)
