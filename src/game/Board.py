from __future__ import annotations

from game.HumanPlayer import HumanPlayer
from game.AiPlayer import AiPlayer
import numpy as np
from typing import List, Optional, Union

PlayerT = Union[HumanPlayer, AiPlayer]
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
    
    def __init__(self,  player1: PlayerT, player2: PlayerT):
        """
        Initialize the game with players and starting state.
        
        Args:
            player1_type: Type of player 1 ("human" or "ai")
            player2_type: Type of player 2 ("human" or "ai")
        """
       
        self.players: List[PlayerT] = []
        self._init_players(player1, player2)

        self.current_player_idx: int = 0
        self.game_over: bool = False
        self.winner: Optional[PlayerT] = None
        self.total_moves: int = 0

        self.game_state: np.ndarray = np.zeros((self.ROWS, self.COLUMNS), np.int8)
        self.board_size = (self.COLUMNS, self.ROWS)
    
    def _init_players(self, p1: PlayerT, p2: PlayerT) -> None:
        """
        Initialize players based on their types.
        
        Args:
            player1_type: Type of player 1
            player2_type: Type of player 2
        """
        self.players.append(p1 if p1.playertype == "AI" else HumanPlayer(1))
        self.players.append(p2 if p2.playertype == "AI" else HumanPlayer(2))


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
        
    def is_valid_column(self, column: int) -> bool:
        """
        Check if a column is valid for placing a piece.
        
        Args:
            column: The column to check (1-7)
            
        Returns:
            Boolean indicating if the column is valid
        """
        return 1 <= column <= self.COLUMNS and self.game_state[0, column - 1] == self.EMPTY

    
    def get_valid_moves(self) -> List[int]:
        """
        Get all valid moves (columns) for the current state.
        
        Returns:
            List of valid columns (1-7)
        """
        return [c for c in range(1, self.COLUMNS + 1) if self.is_valid_column(c)]

    
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
    

    def shallow_copy(self) -> "Board":
        clone: "Board" = object.__new__(Board)          # bypass __init__
        clone.__dict__ = self.__dict__.copy()            # shallow copy of attrs
        clone.game_state = self.game_state.copy()        # *real* board copy
        clone.game_over = False                     # reset
        clone.winner = None                         # reset
        return clone



    def apply_move(self, player_id: int, column: int) -> "Board":
        """Return a brand‑new Board after `player_id` drops in `column`."""
        nxt = self.shallow_copy()
        nxt.place_piece(player_id, column)
        nxt.total_moves += 1

        # terminal detection
        if nxt.detect_win(player_id):
            nxt.game_over = True
            nxt.winner = next(p for p in nxt.players if p.player_id == player_id)
        elif len(nxt.get_valid_moves()) == 0:
            nxt.game_over = True
            nxt.winner = None
        else:
            nxt.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        return nxt


    def detect_win(self, player_id)-> bool:
        """
        Check if the specified player has won.
        
        Args:
            player_id: ID of the player to check for win
            
        Returns:
            Boolean indicating if the player has won
        """
        b = self.game_state
        R, C, W = self.ROWS, self.COLUMNS, self.MAX_SPACE_TO_WIN
        # horizontal / vertical
        for c in range(C - W):
            for r in range(R):
                if all(b[r, c + k] == player_id for k in range(4)):
                    return True
        for c in range(C):
            for r in range(R - W):
                if all(b[r + k, c] == player_id for k in range(4)):
                    return True
        # diagonals
        for c in range(C - W):
            for r in range(R - W):
                if all(b[r + k, c + k] == player_id for k in range(4)):
                    return True
        for c in range(C - W):
            for r in range(W, R):
                if all(b[r - k, c + k] == player_id for k in range(4)):
                    return True
        return False
    

    # evaluation (heuristic)
    def pos_score(self, pid: int) -> int:
        score = 0
        b = self.game_state
        # centre control
        for c in range(2, 5):
            for r in range(self.ROWS):
                if b[r, c] == pid:
                    score += 3 if c == 3 else 2
        # windows of four
        def add_window(rs, cs):
            nonlocal score
            window = [b[r, c] for r, c in zip(rs, cs)]
            score += self._eval_window(window, pid)
        # horiz & vert
        for c in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for r in range(self.ROWS):
                add_window([r]*4, [c+i for i in range(4)])
        for c in range(self.COLUMNS):
            for r in range(self.ROWS - self.MAX_SPACE_TO_WIN):
                add_window([r+i for i in range(4)], [c]*4)
        # diag
        for c in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for r in range(self.ROWS - self.MAX_SPACE_TO_WIN):
                add_window([r+i for i in range(4)], [c+i for i in range(4)])
        for c in range(self.COLUMNS - self.MAX_SPACE_TO_WIN):
            for r in range(self.MAX_SPACE_TO_WIN, self.ROWS):
                add_window([r-i for i in range(4)], [c+i for i in range(4)])
        return score
    
    def _eval_window(self, window, pid):
        opp = 3 - pid
        p, e, o = window.count(pid), window.count(self.EMPTY), window.count(opp)
        if p == 4:             return 100_000
        if p == 3 and e == 1:  return 100
        if p == 2 and e == 2:  return 10
        return 0


    def relative_score(self, my_id: int) -> int:
        return self.pos_score(my_id) - self.pos_score(3 - my_id)


    def get_current_player(self)-> PlayerT:
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
        self.__init__(self.players[0], self.players[1])  # rebuild fresh

    def __str__(self):  # quick text view for debugging
        return "\n".join(" ".join(str(c) for c in row) for row in self.game_state)
    
    
