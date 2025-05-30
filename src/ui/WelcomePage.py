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
        self.ai_difficulty_1 = 2  # Options: "easy", "medium", "hard"
        self.ai_difficulty_2 = 4  # For AI vs AI mode
        
        # Custom difficulty input
        self.custom_difficulty_1 = ""
        self.custom_difficulty_2 = ""
        self.active_input = None  # Which input field is active
        
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
            'title': (70, 70, 120),
            'input_inactive': (220, 220, 220),
            'input_active': (240, 240, 255),
            'input_border': (100, 100, 100)
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
        button_width = 150
        button_height = 30
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
        
        # AI 1 difficulty buttons - align them evenly across the center
        self.buttons.append({
            'id': 'ai1_easy',
            'text': 'AI 1: Easy',
            'rect': pygame.Rect(self.width // 2 - button_width - button_width//2 - margin, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(1, 1),
            'type': 'ai1',
            'selected': self.ai_difficulty_1 == 1
        })
        
        self.buttons.append({
            'id': 'ai1_medium',
            'text': 'AI 1: Medium',
            'rect': pygame.Rect(self.width // 2 - button_width // 2, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(1, 2),
            'type': 'ai1',
            'selected': self.ai_difficulty_1 == 3
        })
        
        self.buttons.append({
            'id': 'ai1_hard',
            'text': 'AI 1: Hard',
            'rect': pygame.Rect(self.width // 2 + button_width//2 + margin, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(1, 5),
            'type': 'ai1',
            'selected': self.ai_difficulty_1 == 5
        })
        
        y_position += button_height + margin 
        
        # Display current AI 1 difficulty 
        self.ai1_depth_y = y_position
        y_position += margin  # Space for the text
        
        # Custom difficulty input for AI 1 - center it better
        input_width = 150
        input_height = 30
        self.custom_input_1_rect = pygame.Rect(self.width // 2 - input_width - margin, y_position, input_width, input_height)
        
        # Button to apply custom difficulty - position right next to the input
        self.buttons.append({
            'id': 'ai1_custom_apply',
            'text': 'Set Custom',
            'rect': pygame.Rect(self.width // 2 + margin, y_position, input_width, input_height),
            'action': self._apply_custom_difficulty_1,
            'type': 'action',
            'selected': False
        })
        
        y_position += input_height + margin * 2
        
        # AI 2 difficulty buttons (for AI vs AI mode)
        self.buttons.append({
            'id': 'ai2_easy',
            'text': 'AI 2: Easy',
            'rect': pygame.Rect(self.width // 2 - button_width - button_width//2 - margin, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(2, 2),
            'type': 'ai2',
            'selected': self.ai_difficulty_2 == 2
        })
        
        self.buttons.append({
            'id': 'ai2_medium',
            'text': 'AI 2: Medium',
            'rect': pygame.Rect(self.width // 2 - button_width // 2, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(2, 4),
            'type': 'ai2',
            'selected': self.ai_difficulty_2 == 4
        })
        
        self.buttons.append({
            'id': 'ai2_hard',
            'text': 'AI 2: Hard',
            'rect': pygame.Rect(self.width // 2 + button_width//2 + margin, y_position, button_width, button_height),
            'action': lambda: self._select_ai_difficulty(2, 6),
            'type': 'ai2',
            'selected': self.ai_difficulty_2 == 6
        })
        
        y_position += button_height + margin
        
        # Display current AI 2 difficulty
        self.ai2_depth_y = y_position
        y_position += margin  # Space for the text
        
        # Custom difficulty input for AI 2 - center it better
        self.custom_input_2_rect = pygame.Rect(self.width // 2 - input_width - margin, y_position, input_width, input_height)
        
        # Button to apply custom difficulty for AI 2 - position right next to the input
        self.buttons.append({
            'id': 'ai2_custom_apply',
            'text': 'Set Custom',
            'rect': pygame.Rect(self.width // 2 + margin, y_position, input_width, input_height),
            'action': self._apply_custom_difficulty_2,
            'type': 'action',
            'selected': False
        })
        
        y_position += input_height + margin
        
        # Start button - position at the bottom with enough space
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
        else:
            self.ai_difficulty_2 = difficulty
    
    def _apply_custom_difficulty_1(self):
        """Apply custom difficulty for AI 1."""
        try:
            if self.custom_difficulty_1.strip():
                difficulty = max(1, min(10, int(self.custom_difficulty_1)))
                self.ai_difficulty_1 = difficulty
                
                # Deselect preset buttons
                for button in self.buttons:
                    if button['type'] == 'ai1':
                        button['selected'] = False
        except ValueError:
            # Invalid input, ignore
            pass
    
    def _apply_custom_difficulty_2(self):
        """Apply custom difficulty for AI 2."""
        try:
            if self.custom_difficulty_2.strip():
                difficulty = max(1, min(10, int(self.custom_difficulty_2)))
                self.ai_difficulty_2 = difficulty
                
                # Deselect preset buttons
                for button in self.buttons:
                    if button['type'] == 'ai2':
                        button['selected'] = False
        except ValueError:
            # Invalid input, ignore
            pass
    
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
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event)

    def _handle_click(self, pos):
        """Handle mouse clicks."""
        # Check for input field clicks
        if self.custom_input_1_rect.collidepoint(pos):
            self.active_input = 1
        elif self.custom_input_2_rect.collidepoint(pos):
            self.active_input = 2
        else:
            self.active_input = None
            
            # Check buttons
            for button in self.buttons:
                if button['rect'].collidepoint(pos):
                    # Mark buttons of the same type as unselected
                    if button['type'] in ['game_mode', 'ai1', 'ai2']:
                        for other_button in self.buttons:
                            if other_button['type'] == button['type']:
                                other_button['selected'] = False
                        button['selected'] = True
                    button['action']()
                    break

    def _handle_key_press(self, event):
        """Handle key presses for text input."""
        if self.active_input is None:
            return
            
        if event.key == pygame.K_BACKSPACE:
            # Remove last character
            if self.active_input == 1:
                self.custom_difficulty_1 = self.custom_difficulty_1[:-1]
            else:
                self.custom_difficulty_2 = self.custom_difficulty_2[:-1]
        elif event.key == pygame.K_RETURN:
            # Apply the custom difficulty
            if self.active_input == 1:
                self._apply_custom_difficulty_1()
            else:
                self._apply_custom_difficulty_2()
            self.active_input = None
        elif event.unicode.isdigit():
            # Only allow digits
            if self.active_input == 1:
                if len(self.custom_difficulty_1) < 2:  # Limit to 2 digits (max 10)
                    self.custom_difficulty_1 += event.unicode
            else:
                if len(self.custom_difficulty_2) < 2:  # Limit to 2 digits (max 10)
                    self.custom_difficulty_2 += event.unicode

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
        ai_rect = ai_text.get_rect(center=(self.width // 2, 200))  # Adjusted y-position to lift it up
        self.screen.blit(ai_text, ai_rect)
        
        # Draw buttons
        for button in self.buttons:
            if (button['type'] == 'ai2' or button['id'] == 'ai2_custom_apply') and self.game_mode != 'ai_vs_ai':
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
        
        # Draw custom difficulty input fields and labels
        # AI 1 custom input
        custom_label = self.font_small.render("Custom Depth:", True, self.colors['text'])
        label_rect = custom_label.get_rect()
        label_rect.right = self.custom_input_1_rect.left - 10  # Position label to the left of the input box
        label_rect.centery = self.custom_input_1_rect.centery
        self.screen.blit(custom_label, label_rect)
        
        input_color = self.colors['input_active'] if self.active_input == 1 else self.colors['input_inactive']
        pygame.draw.rect(self.screen, input_color, self.custom_input_1_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.colors['input_border'], self.custom_input_1_rect, 2, border_radius=5)
        
        text_surf = self.font_small.render(self.custom_difficulty_1, True, self.colors['text'])
        text_rect = text_surf.get_rect()
        text_rect.center = self.custom_input_1_rect.center
        self.screen.blit(text_surf, text_rect)
        
        # Draw current difficulty selections
        ai1_text = self.font_small.render(f"Current AI 1 Depth: {self.ai_difficulty_1}", True, (0, 100, 0))
        ai1_rect = ai1_text.get_rect(center=(self.width // 2, self.ai1_depth_y))
        self.screen.blit(ai1_text, ai1_rect)
        
        # AI 2 custom input (only show in AI vs AI mode)
        if self.game_mode == 'ai_vs_ai':
            custom_label2 = self.font_small.render("Custom Depth:", True, self.colors['text'])
            label_rect2 = custom_label2.get_rect()
            label_rect2.right = self.custom_input_2_rect.left - 10
            label_rect2.centery = self.custom_input_2_rect.centery
            self.screen.blit(custom_label2, label_rect2)
            
            input_color = self.colors['input_active'] if self.active_input == 2 else self.colors['input_inactive']
            pygame.draw.rect(self.screen, input_color, self.custom_input_2_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.colors['input_border'], self.custom_input_2_rect, 2, border_radius=5)
            
            text_surf = self.font_small.render(self.custom_difficulty_2, True, self.colors['text'])
            text_rect = text_surf.get_rect()
            text_rect.center = self.custom_input_2_rect.center
            self.screen.blit(text_surf, text_rect)
            
            ai2_text = self.font_small.render(f"Current AI 2 Depth: {self.ai_difficulty_2}", True, (0, 0, 150))
            ai2_rect = ai2_text.get_rect(center=(self.width // 2, self.ai2_depth_y))
            self.screen.blit(ai2_text, ai2_rect)
        
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
