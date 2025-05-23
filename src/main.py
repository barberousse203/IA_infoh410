# Entry point of the application

from game.Board import Board
from ui.GameGUI import GameGUI
from ui.WelcomePage import WelcomePage

def main():
    # Show welcome page to get game configuration
    welcome = WelcomePage(800, 600)
    config = welcome.run()
    if not config:
        print("Game configuration was not provided.")
        return
    print(f"Starting game with configuration: {config}")

    # Create game with the selected configuration
    game = GameGUI(
        width=800, 
        height=600,
        player1=config['player1'],
        player2=config['player2']
    )
    
    # Run the game
    game.run()

if __name__ == "__main__":
    main()