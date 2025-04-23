import pygame
from game.Board import Board

class GameGUI:
    """
    Game GUI class responsible for displaying the game and handling user interface.
    This class connects the game logic to the visual representation.
    """
    
    def __init__(self, width=800, height=600):
        """
        Initialize the game GUI.
        
        Args:
            width: Width of the game window
            height: Height of the game window
        """
        self.width = width
        self.height = height
        self.screen = None
        self.game = Board()
        self.running = False
        self.clock = None
        self.font = None
        self.colors = {
            'background': (240, 240, 240),
            'text': (0, 0, 0),
            'player1': (255, 0, 0),
            'player2': (0, 0, 255),
            'highlight': (255, 255, 0)
        }
    
    def setup(self):
        """Set up the pygame window and initialize resources."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.running = True
    
    def run(self):
        """Run the main game loop."""
        self.setup()
        
        # Main game loop
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
    
    def _handle_events(self):
        """Handle pygame events like mouse clicks and key presses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse clicks for game interaction
                self._handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                # Handle key presses
                self._handle_key_press(event.key)
    
    def _handle_mouse_click(self, pos):
        """
        Handle mouse click at the given position.
        
        Args:
            pos: (x, y) tuple of mouse position
        """
        # TODO: Convert mouse position to game move and process it
        pass
    
    def _handle_key_press(self, key):
        """
        Handle key press events.
        
        Args:
            key: Key code of the pressed key
        """
        # Example: Reset game when 'r' is pressed
        if key == pygame.K_r:
            self.game.reset_game()
        # Add other key handlers as needed
    
    def _update(self):
        """Update game state."""
        # If current player is AI, get its move
        current_player = self.game.get_current_player()
        if hasattr(current_player, 'is_ai') and current_player.is_ai:
            move = current_player.make_move(self.game.game_state)
            self.game.make_move(move)
        
        # Check if game is over
        if self.game.check_game_over():
            # TODO: Handle game over state
            pass
    
    def _render(self):
        """Render the game state to the screen."""
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Render game board
        self._render_board()
        
        # Render game information (current player, game status, etc)
        self._render_game_info()
    
    def _render_board(self):
        """Render the game board."""
        # TODO: Implement board rendering based on game state
        pass
    
    def _render_game_info(self):
        """Render game information."""
        # Render current player
        current_player = self.game.get_current_player()
        player_text = self.font.render(f"Current: {current_player}", True, self.colors['text'])
        self.screen.blit(player_text, (20, 20))
        
        # Render game status if game is over
        if self.game.game_over:
            winner = self.game.get_winner()
            if winner:
                status_text = self.font.render(f"Winner: {winner}", True, self.colors['text'])
            else:
                status_text = self.font.render("Draw!", True, self.colors['text'])
            self.screen.blit(status_text, (self.width // 2 - 100, 20))
    
    def show_message(self, message, position=(None, None), duration=2000):
        """
        Display a message on the screen.
        
        Args:
            message: Text message to display
            position: (x, y) position tuple, centers if None
            duration: How long to display in milliseconds
        """
        msg_surface = self.font.render(message, True, self.colors['text'])
        x = (self.width - msg_surface.get_width()) // 2 if position[0] is None else position[0]
        y = (self.height - msg_surface.get_height()) // 2 if position[1] is None else position[1]
        
        # TODO: Implement message display with timer
        self.screen.blit(msg_surface, (x, y))
        pygame.display.flip()
