# Entry point of the application

from game.Board import Board
from ui.GameGUI import GameGUI

def main():
    game = GameGUI()
    game.run()

if __name__ == "__main__":
    main()