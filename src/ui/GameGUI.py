import pygame
from game.Board import Board
import time

class GameGUI:
    """
    Game GUI class responsible for displaying the game and handling user interface.
    This class connects the game logic to the visual representation.
    """
    
    def __init__(self, width=800, height=600, player1=None, player2=None):
        """
        Initialize the game GUI.
        
        Args:
            width: Width of the game window
            height: Height of the game window
            player1: Player 1 object (Human or AI)
            player2: Player 2 object (Human or AI)
        """
        self.width = width
        self.height = height
        self.screen = None
        self.game = Board(player1, player2)
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
        self.board_offset_x = 100
        self.board_offset_y = 100
        self.cell_size = 60
        self.board_size = (self.cell_size * self.game.board_size[0], self.cell_size * self.game.board_size[1])
        self.message_start_time = 0
        self.current_message = None
        self.message_duration = 0
        self.turn_count = 0  # Add our own turn counter
    
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
        if self.game.game_over:
            return
            
        # Check if click is within board bounds
        x, y = pos
        if (self.board_offset_x <= x <= self.board_offset_x + self.board_size[0] and
                self.board_offset_y <= y <= self.board_offset_y + self.board_size[1]):
            
            # Convert click to board coordinates
            board_x = (x - self.board_offset_x) // self.cell_size
            # board_y = (y - self.board_offset_y) // self.cell_size
            
            # For Connect Four style games, only the column (board_x) matters
            # Convert to 1-based indexing if that's what the Board class expects
            move = board_x + 1  # Assuming Board uses 1-based column indexing
            
            # Get current player and make the move if it's a human player
            current_player = self.game.get_current_player()
            if current_player.playertype == "Human":
                success = self.game.make_move(move)
                if success:
                    self.turn_count += 1  # Increment turn count on successful move
                if not success:
                    self.show_message("Invalid move! Try again.", duration=1500)

    
    def _handle_key_press(self, key):
        """
        Handle key press events.
        
        Args:
            key: Key code of the pressed key
        """
        # Example: Reset game when 'r' is pressed
        if key == pygame.K_r:
            self.game.reset_game()
            self.turn_count = 0  # Reset turn count
        # Add other key handlers as needed
    
    def _update(self):
        """Update game state."""
        # If current player is AI, get its move
        if not self.game.game_over:
            current_player = self.game.get_current_player()
            if current_player.playertype == "AI":
                try:
                    move = current_player.get_move(self.game)
                    success = self.game.make_move(move)
                    if success:
                        self.turn_count += 1  # Incrémenter le compteur de tours
                    else:
                        self.show_message(f"AI attempted invalid move: {move}")
                except Exception as e:
                    self.show_message(f"AI error: {str(e)}")
        else:
            return # No need to update if game is over
            

        
        # Check if game is over
        if self.game.check_game_over():
            winner = self.game.get_winner()
            if winner:
                self.show_message(f"Game Over! {winner} wins!")
            else:
                self.show_message("Game Over! It's a draw!")
        
        # Check if message should be cleared
        if self.current_message and time.time() - self.message_start_time > self.message_duration / 1000:
            self.current_message = None
    
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
        # Draw the board background
        # Ensure all values are integers for pygame.Rect
        x = int(self.board_offset_x)
        y = int(self.board_offset_y)
        width = int(self.board_size[0])
        height = int(self.board_size[1])
        board_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (200, 200, 200), board_rect)
        
        # Draw grid lines
        for i in range(self.game.board_size[0] + 1):
            # Vertical lines
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (self.board_offset_x + i * self.cell_size, self.board_offset_y),
                (self.board_offset_x + i * self.cell_size, self.board_offset_y + self.board_size[1]),
                2
            )
        
        for i in range(self.game.board_size[1] + 1):
            # Horizontal lines
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (self.board_offset_x, self.board_offset_y + i * self.cell_size),
                (self.board_offset_x + self.board_size[0], self.board_offset_y + i * self.cell_size),
                2
            )
        
        # Draw pieces
        for y in range(self.game.board_size[1]):
            for x in range(self.game.board_size[0]):
                # Access numpy array directly instead of using get_cell
                cell_value = self.game.game_state[y, x]  # Note: NumPy typically uses [row, col] indexing
                
                if cell_value != 0:  # Adjust based on your board representation
                    color = self.colors['player1'] if cell_value == 1 else self.colors['player2']
                    
                    # Draw a piece (circle)
                    center_x = self.board_offset_x + x * self.cell_size + self.cell_size // 2
                    center_y = self.board_offset_y + y * self.cell_size + self.cell_size // 2
                    radius = self.cell_size // 2 - 5
                    pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
    
    def _render_game_info(self):
        """Render game information."""
        # Render current player
        current_player = self.game.get_current_player()
        player_text = self.font.render(f"Current: {current_player}", True, self.colors['text'])
        self.screen.blit(player_text, (20, 20))
        
        # Render turn counter using our own counter
        turn_text = self.font.render(f"Turn: {self.turn_count}", True, self.colors['text'])
        self.screen.blit(turn_text, (20, 60))
        
        # Render game status if game is over
        if self.game.game_over:
            winner = self.game.get_winner()
            if winner:
                status_text = self.font.render(f"Winner: {winner}", True, self.colors['text'])
            else:
                status_text = self.font.render("Draw!", True, self.colors['text'])
            self.screen.blit(status_text, (self.width // 2 - 100, 20))
        
        # Display current message if any
        if self.current_message:
            self._display_current_message()
    
    def _display_current_message(self):
        """Display the current message on screen."""
        if not self.current_message:
            return
            
        msg_surface = self.font.render(self.current_message, True, (50, 50, 150))
        msg_rect = msg_surface.get_rect()
        msg_rect.center = (self.width // 2, self.height - 50)
        
        # Add background box
        padding = 10
        box_rect = msg_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(self.screen, (220, 220, 250), box_rect)
        pygame.draw.rect(self.screen, (50, 50, 150), box_rect, 2)
        
        # Render text
        self.screen.blit(msg_surface, msg_rect)
    
    def show_message(self, message, position=(None, None), duration=2000):
        """
        Display a message on the screen.
        
        Args:
            message: Text message to display
            position: (x, y) position tuple, centers if None
            duration: How long to display in milliseconds
        """
        self.current_message = message
        self.message_start_time = time.time()
        self.message_duration = duration
