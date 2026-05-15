import sys
from src.parse.read_config import parse_config
from src.engine.dataprocess import GameMannager

"""
- Readme
- Makefile:
    -Pygame, Pydantic, Flake8, Mypy.  Y src/map/mazegenerator-00001-py3-none-any
    (Instalar Maze como un Paquete)
- Limitar Altura y anchura del config.json. Por que tiene Recursiva el Maze.
- Loop_instructions: Anadir nuevos comandos explicar Cheat mode.
- Loop_end: Hacerlo escala independiente
- In-Game HUD (always visible during gameplay).
    - self.game_mannager.level_time
    - self.game_mannager.player.lives
- loop_game -> def draw:
        Modificarlo todo
     Assets: Pacman
        Class Ghost -> self.mode == "escape" (Fantasmas en azul).
- Docstrings
- Flake8, Mypy
"""
def main() -> None:
    try :
        if len(sys.argv) != 2:
            raise ValueError("[ERROR] Need only 1 argument")
        data = parse_config(sys.argv[1])
        game = GameMannager(data)
        game.run()
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
