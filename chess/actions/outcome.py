import numpy as np
from typing import Dict, Optional, Self

from chess.chess_types import Position, Vector, Direction
from chess.chess_types import Loyalty, Piece
from chess.chess_types import DirCls as D

from chess.units.get_piece import get_piece_class

class Outcome:
    """
    Represents a change in board state.
    """
    
    # TODO: Store some info that could be used to preview the action?
    # prev_dict: Dict[Piece, Optional[Position]] = {}
    # TODO: Could also contain code to render this preview?
    #       With a lerp value?
    
    def __init__(self, *args, **kwargs):
        pass

    def realize(self, board):
        """
        Apply this outcome to the board state.
        """
        pass
    
    # TODO: This would be neat.
    def preview(self, board):
        """
        Preview the action.
        """
        pass


class Move(Outcome):
    piece: object
    target: Position
    
    def __init__(self, piece, target: Position):
        super().__init__()
        self.piece = piece
        self.target = target
    
    def realize(self, board):
        self.piece.move(self.target) # TODO: Go through board?
        
class Capture(Move):
    captured: object
    
    def __init__(self, piece, target: Position, captured: object):
        super().__init__(piece, target)
        self.captured = captured
    
    def realize(self, board):
        super().realize(board)
        # board.remove_piece(self.captured)


class Promote(Move): # TODO: Could be capture???
    promoted_to: Piece
    def __init__(self, piece, target: Position, promoted_to: Piece = Piece.QUEEN):
        super().__init__(piece, target)
        self.promoted_to = promoted_to
        
    def realize(self, board):
        super().realize(board)
        t = board.get_tile(self.target)
        new_piece = get_piece_class(self.promoted_to)(board, self.piece.loyalty, self.target)
        t.piece = new_piece

class Castle(Outcome):
    king_piece: object
    rook_piece: object
    
    def __init__(self, king_piece, rook_piece):
        super().__init__()
        self.king_piece = king_piece
        self.rook_piece = rook_piece
    
    def realize(self, board):
        print('TODO: IMPLEMENT CASTLE')
        # self.piece.move(self.target)
        # self.rook.move(self.rook_target)