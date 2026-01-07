import sys
from game import Mode, Game

def main():
    argc = len(sys.argv)
    if argc != 2:
        print("missing command line arguments")
        print("First Usage: python ./main.py player_mode")
        print("First Usage: python ./main.py algorithm_and_player_mode")
        print("First Usage: python ./main.py algorithm_mode")
        sys.exit(1)
    try:
        match (sys.argv[1].lower):
            case "player_mode":
                game = Game(Mode.PLAYER_MODE)
            case "algorithm_and_player_mode":
                game = Game(Mode.ALGORITHM_AND_PLAYER_MODE)
            case "algorithm_mode":
                game = Game(Mode.ALGORITHM_MODE)
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
