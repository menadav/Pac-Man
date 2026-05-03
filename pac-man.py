import sys
from src.parse.read_config import parse_config
from src.engine.loop_game import GameMannager

def main() -> None:
    try :
        if len(sys.argv) != 2:
            raise ValueError("[ERROR] Need only 1 argument")
        data = parse_config(sys.argv[1])
        game = Game(data)
        game.run()
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
