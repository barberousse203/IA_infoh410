import pygame
import sys
from game.HumanPlayer import HumanPlayer
from game.AiPlayer import AiPlayer

class WelcomePage:
    """
    Welcome page for the game that allows selecting game modes and AI difficulty.
    """
    
    def __init__(self, width=800, height=600):
        """
        Initialize the welcome page.
        
        Args:
            width: Width of the window
            height: Height of the window
        """
        self.width = width
        self.height = height
        self.screen = None
        self.font_large = None
        self.font_medium = None
        self.font_small = None
        self.running = True
        self.clock = None
        
        # Game configuration options
        self.game_mode = "human_vs_ai"  # Options: "human_vs_ai", "ai_vs_ai"
        self.ai_difficulty_1 = "medium"  # Options: "easy", "medium", "hard"
        self.ai_difficulty_2 = "medium"  # For AI vs AI mode
        
        # UI Elements
        self.buttons = []
        self.selected_option = None
        
        # Colors
        self.colors = {
            'background': (240, 240, 240),
            'text': (20, 20, 20),
            'button': (70, 130, 180),
            'button_hover': (100, 160, 210),
            'button_text': (255, 255, 255),
            'selected': (50, 205, 50),
            'title': (70, 70, 120)
        }
        
    def setup(self):
        """Set up the pygame window and initialize resources."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game Setup")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont(None, 56)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 28)
        self._create_buttons()
        
    def _create_buttons(self):
        """Create buttons for the welcome page."""
        button_width = 200
        button_height = 50
        margin = 20
        y_position = 150
        
        # Game mode buttons
        self.buttons.append({
            'id': 'human_vs_ai',
            'text': 'Human vs AI',
            'rect': pygame.Rect(self.width // 2 - button_width - margin // 2, y_position, button_width, button_height),
            'action': lambda: self._select_game_mode('human_vs_ai'),
            'type': 'game_mode',
            'selected': self.game_mode == 'human_vs_ai'
        })
        
        self.buttons.append({
            'id': 'ai_vs_ai',
            'text': 'AI vs AI',
            'rect': pygame.Rect(self.width // 2 + margin // 2, y_position, button_width, button_height),
            'action': lambda: self._select_game_mode('ai_vs_ai'),
            'type': 'game_mode',
            'selected': self.game_mode == 'ai_vs_ai'
        })
        
        y_position += button_height + margin * 2
        
        # AI 1 difficulty buttons
        self.buttons.append({
            'id': 'ai1_easy',
            'text': 'AI 1: Easy',
            'rect': pygame.Rect(self.width // 2 - button_width*3/2 - margin, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(1, 'easy'),
            'type': 'ai1',
            'selected': self.ai_difficulty_1 == 1
        })
        
        self.buttons.append({
            'id': 'ai1_medium',
            'text': 'AI 1: Medium',
            'rect': pygame.Rect(self.width // 2 - button_width // 2, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(1, 'medium'),
            'type': 'ai1',
            'selected': self.ai_difficulty_1 == 3
        })
        
        self.buttons.append({
            'id': 'ai1_hard',
            'text': 'AI 1: Hard',
            'rect': pygame.Rect(self.width // 2 + button_width // 2 + margin, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(1, 'hard'),
            'type': 'ai1',
            'selected': self.ai_difficulty_1 == 5
        })
        
        y_position += button_height + margin * 2
        
        # AI 2 difficulty buttons (for AI vs AI mode)
        self.buttons.append({
            'id': 'ai2_easy',
            'text': 'AI 2: Easy',
            'rect': pygame.Rect(self.width // 2 - button_width*3/2 - margin, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(2, 'easy'),
            'type': 'ai2',
            'selected': self.ai_difficulty_2 == 2
        })
        
        self.buttons.append({
            'id': 'ai2_medium',
            'text': 'AI 2: Medium',
            'rect': pygame.Rect(self.width // 2 - button_width // 2, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(2, 'medium'),
            'type': 'ai2',
            'selected': self.ai_difficulty_2 == 4
        })
        
        self.buttons.append({
            'id': 'ai2_hard',
            'text': 'AI 2: Hard',
            'rect': pygame.Rect(self.width // 2 + button_width // 2 + margin, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(2, 'hard'),
            'type': 'ai2',
            'selected': self.ai_difficulty_2 == 6
        })
        
        y_position += button_height + margin * 3
        
        # Start button
        self.buttons.append({
            'id': 'start_game',
            'text': 'Start Game',
            'rect': pygame.Rect(self.width // 2 - button_width // 2, y_position, button_width, button_height),
            'action': self._start_game,
            'type': 'action',
            'selected': False
        })
    
    def _select_game_mode(self, mode):
        """Select a game mode."""
        self.game_mode = mode
        # Update button states
        for button in self.buttons:
            if button['type'] == 'game_mode':
                button['selected'] = button['id'] == mode
    
    def _select_ai_difficulty(self, ai_number, difficulty):
        """Select AI difficulty."""
        if ai_number == 1:
            self.ai_difficulty_1 = difficulty
            for button in self.buttons:
                if button['type'] == 'ai1':
                    button['selected'] = button['id'] == f'ai1_{difficulty}'
        else:
            self.ai_difficulty_2 = difficulty
            for button in self.buttons:
                if button['type'] == 'ai2':
                    button['selected'] = button['id'] == f'ai2_{difficulty}'
    
    def _start_game(self):
        """Start the game with the selected options."""
        self.running = False
    
    def run(self):
        """Run the welcome page."""
        self.setup()
        
        while self.running:
            self._handle_events()
            self._render()
            pygame.display.flip()
            self.clock.tick(60)
        
        # Return the selected configuration
        return self._get_game_config()
    
    def _handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self._handle_click(event.pos)
    
    def _handle_click(self, pos):
        """Handle mouse clicks."""
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                button['action']()
                break
    
    def _render(self):
        """Render the welcome page."""
        self.screen.fill(self.colors['background'])
        
        # Draw title
        title_text = self.font_large.render("Game Setup", True, self.colors['title'])
        title_rect = title_text.get_rect(center=(self.width // 2, 60))
        self.screen.blit(title_text, title_rect)
        
        # Draw game mode text
        mode_text = self.font_medium.render("Select Game Mode:", True, self.colors['text'])
        mode_rect = mode_text.get_rect(center=(self.width // 2, 120))
        self.screen.blit(mode_text, mode_rect)
        
        # Draw AI text
        if self.game_mode == 'human_vs_ai':
            ai_text = self.font_medium.render("Select AI Difficulty:", True, self.colors['text'])
        else:
            ai_text = self.font_medium.render("Select AI Players Difficulty:", True, self.colors['text'])
        ai_rect = ai_text.get_rect(center=(self.width // 2, 220))
        self.screen.blit(ai_text, ai_rect)
        
        # Draw buttons
        for button in self.buttons:
            if (button['type'] == 'ai2' and self.game_mode != 'ai_vs_ai'):
                # Hide AI 2 settings if not in AI vs AI mode
                continue
                
            color = self.colors['selected'] if button['selected'] else self.colors['button']
            
            # Check if mouse is over the button
            mouse_pos = pygame.mouse.get_pos()
            if button['rect'].collidepoint(mouse_pos) and not button['selected']:
                color = self.colors['button_hover']
                
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=5)
            pygame.draw.rect(self.screen, (50, 50, 50), button['rect'], 2, border_radius=5)
            
            button_text = self.font_small.render(button['text'], True, self.colors['button_text'])
            text_rect = button_text.get_rect(center=button['rect'].center)
            self.screen.blit(button_text, text_rect)
        
        # Draw explanation text at bottom
        explain_text = self.font_small.render("Choose your game mode and AI difficulty, then click Start Game", 
                                             True, self.colors['text'])
        explain_rect = explain_text.get_rect(center=(self.width // 2, self.height - 50))
        self.screen.blit(explain_text, explain_rect)
            
    def _get_game_config(self):
        """Get the game configuration based on selected options."""
        player1 = None
        player2 = None
        
        if self.game_mode == 'human_vs_ai':
            player1 = HumanPlayer(1)
            player2 = AiPlayer(2, self.ai_difficulty_1)
        else:  # AI vs AI
            player1 = AiPlayer(1, self.ai_difficulty_1)
            player2 = AiPlayer(2, self.ai_difficulty_2)
            
        return {
            'mode': self.game_mode,
            'player1': player1,
            'player2': player2
        }
