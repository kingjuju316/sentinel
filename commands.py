"""
Commands module — handles text commands typed in the terminal.
To add a new command:
  1. Add an entry to COMMANDS (shown automatically in help).
  2. Add a matching elif branch in run_loop().
"""

from __future__ import annotations

import ast
import datetime
import math
import operator as op
from typing import TYPE_CHECKING

from sentinel.modules import BaseModule

if TYPE_CHECKING:
    from sentinel.core.system import System


# Registry of every available command and its description (shown in help).
# Order here is the order shown by the 'help' command.
COMMANDS: dict[str, str] = {
    "online":          "Check if Sentinel is online",
    "status":          "Show system status",
    "time":            "Show current time",
    "date":            "Show today's date",
    "calculate [expr]": "Evaluate a math expression",
    "help":            "Show this list",
    "exit":            "Close Sentinel",
}


class CommandModule(BaseModule):
    name = "commands"

    def __init__(self, system: "System") -> None:
        self._system = system

    # ------------------------------------------------------------------
    # Main loop (blocks until 'exit')
    # ------------------------------------------------------------------

    def run_loop(self) -> None:
        while True:
            try:
                raw = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                self._system.stop()
                break

            cmd = raw.lower()

            if cmd == "":
                continue
            elif cmd == "online":
                self._respond("Sentinel is online and ready.")
            elif cmd == "status":
                self._respond(
                    "All systems operational. "
                    "Microphone listening or standby. "
                    "Status online, ready for your command."
                )
            elif cmd == "time":
                now = datetime.datetime.now()
                self._respond(f"The time is {now.strftime('%-I:%M %p')}.")
            elif cmd == "date":
                today = datetime.date.today()
                self._respond(f"Today is {today.strftime('%A, %B %-d, %Y')}.")
            elif cmd.startswith("calculate"):
                expr = cmd[len("calculate"):].strip()
                self._respond(self._calculate(expr))
            elif cmd == "help":
                self._show_help()
            elif cmd == "exit":
                self._system.stop()
                break
            else:
                print(f"  Unknown command '{raw}'.  Type 'help' for a list.")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _respond(self, text: str) -> None:
        """Print a reply and speak it (if TTS is available)."""
        print(text)
        self._system.voice.say(text)

    def _show_help(self) -> None:
        print("\nAvailable commands:")
        for name, desc in COMMANDS.items():
            print(f"  {name:<10} — {desc}")
        print()

    def _calculate(self, expr: str) -> str:
        """Safely evaluate a math expression — supports +, -, *, /, (), decimals."""
        if not expr:
            return "Please provide an expression. Example: calculate 5 + 3 * 2"

        # Accept spoken words as well as symbols
        expr = (expr
                .replace("multiplied by", "*")
                .replace("divided by", "/")
                .replace("plus", "+")
                .replace("minus", "-")
                .replace("times", "*")
                .replace("over", "/")
                .replace("point", "."))

        SAFE_OPS = {
            ast.Add:  op.add,
            ast.Sub:  op.sub,
            ast.Mult: op.mul,
            ast.Div:  op.truediv,
        }

        def _eval(node: ast.AST) -> float:
            if isinstance(node, ast.Expression):
                return _eval(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return float(node.value)
            if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPS:
                return SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
                val = _eval(node.operand)
                return -val if isinstance(node.op, ast.USub) else val
            raise ValueError(f"Unsupported: {type(node).__name__}")

        try:
            tree = ast.parse(expr.strip(), mode="eval")
            result = _eval(tree)
            if not math.isfinite(result):
                return "That expression has no finite answer."
            formatted = int(result) if result == int(result) else round(result, 10)
            return f"The answer is {formatted}."
        except Exception:
            return f"I couldn't calculate '{expr.strip()}'. Try: calculate 5 + 3 * 2"

    def run(self) -> None:
        pass
