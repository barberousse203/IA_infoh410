import random
import math
import time

class AiPlayer:
    """
    AI player for Connect Four using minimax algorithm with alpha-beta pruning.
    """
    
    def __init__(self, player_id, difficulty=5):
        """
        Initialize AI player.
        
        Args:
            player_id: Player's ID number (1 or 2)
            difficulty: Depth for minimax algorithm (default 5)
        """
        self.player_id = player_id
        self.playertype = "AI"
        self.name = f"Player {player_id} (AI)"
        self.opponent_id = 3 - player_id  # Toggle between 1 and 2
        self.difficulty = difficulty
        self.last_move_time = 0
        self.move_times = []
        
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
        col, _ = self.minimax(board, self.difficulty, -math.inf, math.inf, True)

        # Record the time taken
        self.last_move_time = time.time() - start_time
        self.move_times.append(self.last_move_time)
        
        return col

    def minimax(self, board, depth, alpha, beta, maximizing_player):
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
        valid_moves = board.get_valid_moves()
        game_over = board.check_game_over() or len(valid_moves) == 0
        # Terminal cases
        if depth == 0 or game_over:
            if game_over:
                winner = board.get_winner()
                if winner and winner.player_id == self.player_id:
                    return (None, 1000000000)  # AI wins
                elif winner:
                    return (None, -1000000000)  # Opponent wins
                else:
                    return (None, 0)  # Draw
            else:
                return (None, board.evaluate_position(self.player_id))  # Evaluate board

        col = None
        if maximizing_player:
            value = -math.inf
            for c in valid_moves:
                # Create a copy of the board with this move
                new_board = board.copy()
                new_board.game_state = board.get_successor_state(self.player_id, c)
                new_board.current_player_idx = board.current_player_idx

                # Recursively call minimax

                _, new_score = self.minimax(new_board, depth - 1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    col = c

                if value > alpha:
                    alpha = new_score
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return col, value

        else:  # Minimizing player
            value = math.inf
            for c in valid_moves:
                # Create a copy of the board with this move
                new_board = board.copy()
                new_board.game_state = board.get_successor_state(self.opponent_id, c)
                new_board.current_player_idx = board.current_player_idx

                # Recursively call minimax
                _, new_score = self.minimax(new_board, depth - 1, alpha, beta, True)

                if new_score < value:
                    value = new_score
                    col = c

                if value < beta:
                    beta = value
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return col, value

    def get_average_move_time(self):
        """
        Get the average time taken per move.
        
        Returns:
            Average time in seconds
        """
        if not self.move_times:
            return 0
        return sum(self.move_times) / len(self.move_times)
    
    def get_last_move_time(self):
        """
        Get the time taken for the last move.
        
        Returns:
            Time in seconds
        """
        return self.last_move_time
    
    def set_difficulty(self, difficulty):
        """
        Set the AI difficulty (minimax depth).
        
        Args:
            difficulty: New depth for minimax
        """
        self.difficulty = difficulty
