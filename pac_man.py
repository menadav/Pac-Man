"""Punto de entrada de Pac-Man.

Uso:
    python3 pac_man.py <config.json>
"""

import sys

from src.engine.dataprocess import GameMannager
from src.parse.read_config import parse_config


def main() -> None:
    """Execute the main game loop using the provided configuration file.

    Validates command line arguments, parses the game settings, and starts
    the game manager while handling exceptions to prevent sudden crashes.
    """
    try:
        if len(sys.argv) != 2:
            raise ValueError("[ERROR] Usage: python3 pac_man.py <config.json>")
        data = parse_config(sys.argv[1])
        game = GameMannager(data)
        game.run()
    except ValueError as exc:
        print(exc)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user. Bye!")
        sys.exit(0)
    except Exception as exc:
        print(f"[ERROR] Unexpected failure: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
