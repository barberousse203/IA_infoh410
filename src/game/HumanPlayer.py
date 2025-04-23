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
        self.playertype = "Human"
        self.name = f"Player {player_id} (Human)"
        self.pending_move = None  # Store move from UI until consumed
    
    def __str__(self):
        return self.name
