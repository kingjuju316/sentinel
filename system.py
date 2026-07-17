"""
Core system controller.
All startup/shutdown logic lives here.
Add new subsystems to _load_modules() as the app grows.
"""

from sentinel.config import APP_NAME, VERSION
from sentinel.modules import ModuleRegistry
from sentinel.modules.voice import VoiceModule
from sentinel.modules.commands import CommandModule


class System:
    def __init__(self) -> None:
        self.registry = ModuleRegistry()
        self.voice = VoiceModule()
        self.commands = CommandModule(self)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        print(f"{APP_NAME} online  (v{VERSION})")
        self.voice.say(f"{APP_NAME} online, ready for your command.")
        self._load_modules()
        print("Type 'help' for a list of commands.\n")
        self.commands.run_loop()

    def stop(self) -> None:
        print(f"{APP_NAME} shutting down.")

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _load_modules(self) -> None:
        """
        Register built-in modules here.
        Example:
            from sentinel.modules.monitor import MonitorModule
            self.registry.register(MonitorModule())
        """
        pass
