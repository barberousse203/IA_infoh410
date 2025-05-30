import random
import math
import time
from typing import Tuple

class AiPlayer:
    """
    AI player for Connect Four using minimax algorithm with alpha-beta pruning.
    """
    
    def __init__(self, player_id: int, depth: int = 5):
        """
        Initialize AI player.
        
        Args:
            player_id: Player's ID number (1 or 2)
            difficulty: Depth for minimax algorithm (default 5)
        """
        self.player_id = player_id
        self.opponent_id = 3 - player_id
        self.name = f"Player {player_id} (AI)"
        self.playertype = "AI"
        self.depth = depth
        self.move_times = []
        self.last_move_time = 0.0
        
    def get_move(self, board):
        """
        Get AI's next move using minimax algorithm.
        
        Args:
            board: The game board object
            
        Returns:
            Column number for the next move (1-7)
        """
        start_time = time.time()
        
        # Get the best move using minimax with alpha-beta pruning
        col, _ = self._minimax(board, self.depth, -math.inf, math.inf, True)

        # Record the time taken
        self.last_move_time = time.time() - start_time
        self.move_times.append(self.last_move_time)
        
        return col

    def _minimax(self, board, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[int, float]:
        """
        Minimax algorithm with alpha-beta pruning.

        Args:
            board: The game board object
            depth: Current depth in the search tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: Boolean, True if current player is maximizing

        Returns:
            Tuple (column, score) for the best move
        """
        # terminal / horizon
        if depth == 0 or board.game_over:
            return None, board.relative_score(self.player_id)

        valid_moves = board.get_valid_moves()
        if not valid_moves:  # safety net (should be caught by game_over)
            return None, board.relative_score(self.player_id)

        best_col = random.choice(valid_moves)  # fallback if all equal

        if maximizing:
            value = -math.inf
            for c in valid_moves:
                child = board.apply_move(self.player_id, c)
                _, score = self._minimax(child, depth - 1, alpha, beta, False)
                if score > value:
                    value, best_col = score, c
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # β‑cutoff
            return best_col, value
        else:  # minimizing (opponent)
            value = math.inf
            for c in valid_moves:
                child = board.apply_move(self.opponent_id, c)
                _, score = self._minimax(child, depth - 1, alpha, beta, True)
                if score < value:
                    value, best_col = score, c
                beta = min(beta, value)
                if beta <= alpha:
                    break  # α‑cutoff
            return best_col, value


    def get_average_move_time(self):
        """
        Get the average time taken per move.
        
        Returns:
            Average time in seconds
        """
        return sum(self.move_times) / len(self.move_times) if self.move_times else 0.0

    def __str__(self):
        return self.name
    
