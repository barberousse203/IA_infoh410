class HumanPlayer:
    """
    Human Player implementation for game interactions.
    This class handles the interface between a human player and the game.
    """
    
    def __init__(self, player_id):
        """
        Initialize the human player.
        
        Args:
            player_id: Identifier for the player in the game
        """
        self.player_id = player_id
        self.name = f"Player {player_id}"
    
    def make_move(self, game_state):
        """
        Get and process user input to determine the next move.
        
        Args:
            game_state: Current state of the game
            
        Returns:
            The move selected by the human player
        """
        # TODO: Implement user input handling
        return None
    
    
    def get_input(self, prompt_message="Enter your move: "):
        """
        Get input from the human player.
        
        Args:
            prompt_message: Message to display when requesting input
            
        Returns:
            User input string
        """
        return input(prompt_message)
    
    def __str__(self):
        return self.name
