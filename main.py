import sys
from game import Mode, Game

def main():

    sys.setrecursionlimit(10000)
    argc = len(sys.argv)
    if argc != 2:
        print("missing command line arguments")
        print("First Usage: python ./main.py player_mode")
        print("Second Usage: python ./main.py algorithm_mode")
        print("Third Usage: python ./main.py algorithm_and_player_mode")
        print("Fourth Usage: python ./main.py algorithm_and_random_mode")
        sys.exit(1)
    
    mode_input = sys.argv[1].lower()
    try:
        if mode_input == "player_mode":
            game = Game(Mode.PLAYER_MODE)
        elif mode_input == "algorithm_mode":
            game = Game(Mode.ALGORITHM_MODE)
        elif mode_input == "algorithm_and_player_mode":
            game = Game(Mode.ALGORITHM_AND_PLAYER_MODE)
        elif mode_input == "algorithm_and_random_mode":
            game = Game(Mode.ALGORITHM_AND_RANDOM_MODE)
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    game.run()

if __name__ == '__main__':
    main()
