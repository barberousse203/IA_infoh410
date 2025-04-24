from game.HumanPlayer import HumanPlayer
from game.AiPlayer import AiPlayer
import numpy as np

class Board:
    """
    Main game controller class.
    This class manages the game state, players, and game logic for Connect Four.
    """
    
    # Board dimensions
    ROWS = 6
    COLUMNS = 7
    EMPTY = 0
    MAX_SPACE_TO_WIN = 3  # Farthest space where a winning connection may start
    
    def __init__(self, player1, player2):
        """
        Initialize the game with players and starting state.
        
        Args:
            player1_type: Type of player 1 ("human" or "ai")
            player2_type: Type of player 2 ("human" or "ai")
        """
        self.players = []
        self._init_players(player1, player2)
        self.current_player_idx = 0
        self.game_state = None
        self.game_over = False
        self.winner = None
        self.total_moves = 0
        self.board_size = (self.COLUMNS, self.ROWS)
        self._init_game_state()
    
    def _init_players(self, player1, player2):
        """
        Initialize players based on their types.
        
        Args:
            player1_type: Type of player 1
            player2_type: Type of player 2
        """
        # Player 1
        if player1.playertype == "Human":
            self.players.append(HumanPlayer(1))
        else:
            self.players.append(player1)
            
        # Player 2
        if player2.playertype == "Human":
            self.players.append(HumanPlayer(2))
        else:
            self.players.append(player2)
        
    
    def _init_game_state(self):
        """Initialize the starting game state with an empty board."""
        self.game_state = np.zeros((self.ROWS, self.COLUMNS), np.int8)
    
    def make_move(self, column):
        """
        Apply a move to the game state by placing a piece in the specified column.
        
        Args:
            column: The column to place a piece (1-7)
            
        Returns:
            Boolean indicating if the move was successful
        """
        if not self.is_valid_column(column):
            return False
            
        current_player = self.get_current_player()
        self.place_piece(current_player.player_id, column)
        self.total_moves += 1
        
        # Check if this move resulted in a win
        if self.detect_win(current_player.player_id):
            self.game_over = True
            self.winner = current_player
            return True
            
        # Check if board is full (draw)
        if len(self.get_valid_moves()) == 0:
            self.game_over = True
            return True
            
        # Move to next player's turn
        self.next_turn()
        return True
    
    def is_valid_column(self, column):
        """
        Check if a column is valid for placing a piece.
        
        Args:
            column: The column to check (1-7)
            
        Returns:
            Boolean indicating if the column is valid
        """
        if column < 1 or column > self.COLUMNS:
            return False
        return self.game_state[0][column - 1] == self.EMPTY
    
    def get_valid_moves(self):
        """
        Get all valid moves (columns) for the current state.
        
        Returns:
            List of valid columns (1-7)
        """
        valid_moves = []
        for i in range(1, self.COLUMNS + 1):
            if self.is_valid_column(i):
                valid_moves.append(i)
        return valid_moves
    
    def place_piece(self, player_id, column):
        """
        Place a player's piece in the specified column.
        
        Args:
            player_id: ID of the player (1 or 2)
            column: Column to place the piece (1-7)
        """
        index = column - 1
        for row in reversed(range(self.ROWS)):
            if self.game_state[row][index] == self.EMPTY:
                self.game_state[row][index] = player_id
                return
    
    def get_successor_state(self, player_id, column):
        """
        Get a new board state that would result from placing a piece.
        
        Args:
            player_id: ID of the player making the move
            column: Column to place the piece
            
        Returns:
            New board state as numpy array
        """
        new_board = self.game_state.copy()
        index = column - 1
        for row in reversed(range(self.ROWS)):
            if new_board[row][index] == self.EMPTY:
                new_board[row][index] = player_id
                break
        return new_board
    
    def detect_win(self, player_id):
        """
        Check if the specified player has won.
        
        Args:
            player_id: ID of the player to check for win
            
        Returns:
            Boolean indicating if the player has won
        """
        board = self.game_state
        # Horizontal win
        for col in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for row in range(self.ROWS):
                if board[row][col] == player_id and board[row][col+1] == player_id and \
                   board[row][col+2] == player_id and board[row][col+3] == player_id:
                    return True
                    
        # Vertical win
        for col in range(self.COLUMNS):
            for row in range(self.ROWS - self.MAX_SPACE_TO_WIN):
                if board[row][col] == player_id and board[row+1][col] == player_id and \
                   board[row+2][col] == player_id and board[row+3][col] == player_id:
                    return True
                    
        # Diagonal upwards win
        for col in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for row in range(self.ROWS - self.MAX_SPACE_TO_WIN):
                if board[row][col] == player_id and board[row+1][col+1] == player_id and \
                   board[row+2][col+2] == player_id and board[row+3][col+3] == player_id:
                    return True
                    
        # Diagonal downwards win
        for col in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for row in range(self.MAX_SPACE_TO_WIN, self.ROWS):
                if board[row][col] == player_id and board[row-1][col+1] == player_id and \
                   board[row-2][col+2] == player_id and board[row-3][col+3] == player_id:
                    return True
                    
        return False
    
    def get_current_player(self):
        """
        Get the current player.
        
        Returns:
            Current player object
        """
        return self.players[self.current_player_idx]
    
    def next_turn(self):
        """Switch to the next player's turn."""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def check_game_over(self):
        """
        Check if the game is over.
        
        Returns:
            Boolean indicating if the game is over
        """
        return self.game_over
    
    def get_winner(self):
        """
        Get the winner of the game.
        
        Returns:
            Player who won the game, or None if draw/not over
        """
        return self.winner
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.current_player_idx = 0
        self.game_over = False
        self.winner = None
        self.total_moves = 0
        self._init_game_state()

    def evaluate_position(self, player_id):
        """
        Evaluate the current board position for the given player.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Numeric score representing position value
        """
        score = 0
        board = self.game_state
        
        # Give more weight to center columns
        for col in range(2, 5):
            for row in range(self.ROWS):
                if board[row][col] == player_id:
                    if col == 3:
                        score += 3
                    else:
                        score += 2
        
        # Check all possible four-in-a-row positions
        # Horizontal pieces
        for col in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for row in range(self.ROWS):
                adjacent_pieces = [board[row][col], board[row][col+1], 
                                   board[row][col+2], board[row][col+3]]
                score += self._evaluate_adjacent_pieces(adjacent_pieces, player_id)
        
        # Vertical pieces
        for col in range(self.COLUMNS):
            for row in range(self.ROWS - self.MAX_SPACE_TO_WIN):
                adjacent_pieces = [board[row][col], board[row+1][col], 
                                   board[row+2][col], board[row+3][col]]
                score += self._evaluate_adjacent_pieces(adjacent_pieces, player_id)
        
        # Diagonal upwards pieces
        for col in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for row in range(self.ROWS - self.MAX_SPACE_TO_WIN):
                adjacent_pieces = [board[row][col], board[row+1][col+1], 
                                   board[row+2][col+2], board[row+3][col+3]]
                score += self._evaluate_adjacent_pieces(adjacent_pieces, player_id)
        
        # Diagonal downwards pieces
        for col in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for row in range(self.MAX_SPACE_TO_WIN, self.ROWS):
                adjacent_pieces = [board[row][col], board[row-1][col+1], 
                                   board[row-2][col+2], board[row-3][col+3]]
                score += self._evaluate_adjacent_pieces(adjacent_pieces, player_id)
        
        return score
    
    def _evaluate_adjacent_pieces(self, adjacent_pieces, player_id):
        """
        Evaluate a set of four adjacent positions.
        
        Args:
            adjacent_pieces: List of four adjacent board positions
            player_id: ID of the player
            
        Returns:
            Score for this set of positions
        """
        opponent_id = 3 - player_id  # Toggle between 1 and 2
        score = 0
        
        player_pieces = adjacent_pieces.count(player_id)
        empty_spaces = adjacent_pieces.count(self.EMPTY)
        opponent_pieces = adjacent_pieces.count(opponent_id)
        
        if player_pieces == 4:
            score += 99999
        elif player_pieces == 3 and empty_spaces == 1:
            score += 100
        elif player_pieces == 2 and empty_spaces == 2:
            score += 10
            
        return score
    
    def get_state(self):
        """
        Get the current game state.
        
        Returns:
            Current board state as numpy array
        """
        return self.game_state
    
    def get_total_moves(self):
        """
        Get the total number of moves made in the game so far.
        
        Returns:
            Integer count of moves
        """
        return self.total_moves

    def copy(self):
        """
        Create a deep copy of the board object.

        Returns:
            A new instance of the board with the same state.
        """
        new_board = type(self)(self.players[0], self.players[1])  # Create a new instance of the same class
        new_board.game_state = self.game_state.copy()  # Use numpy's copy method for deep copying
        new_board.current_player_idx = self.current_player_idx  # Copy the current player index
        new_board.game_over = self.game_over  # Copy the game over state
        new_board.winner = self.winner  # Copy the winner
        new_board.total_moves = self.total_moves  # Copy the total moves
        return new_board
