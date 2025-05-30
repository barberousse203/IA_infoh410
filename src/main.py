# Entry point of the application

from game.Board import Board
from ui.GameGUI import GameGUI
from ui.WelcomePage import WelcomePage

def main():
    restart = True
    
    while restart:
        # Show welcome page to get game configuration
        welcome = WelcomePage(800, 600)
        config = welcome.run()
        if not config:
            print("Game configuration was not provided.")
            break
        print("\n" + "="*40)
        print(" Starting Game with Configuration ")
        print("="*40)
        print(f" Mode: {config['mode']}")
        print(f" Player 1: {config['player1']}")
        print(f" Player 2: {config['player2']}")
        print("="*40 + "\n")

        # Create game with the selected configuration
        game = GameGUI(
            width=800, 
            height=600,
            player1=config['player1'],
            player2=config['player2']
        )
        
        # Run the game and check if user wants to return to menu
        restart = game.run()

if __name__ == "__main__":
    main()