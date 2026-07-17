"""
Sentinel — Entry point.
Run: python main.py
"""

from sentinel.core.system import System


def main() -> None:
    system = System()
    system.start()


if __name__ == "__main__":
    main()
