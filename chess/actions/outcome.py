import numpy as np
from typing import Dict, Optional, Self

from chess.chess_types import Position, Vector, Direction
from chess.chess_types import Loyalty, PieceType
from chess.chess_types import DirCls as D

# from chess.units.get_piece import get_piece_class

class Outcome:
    """
    Represents a change in board state.
    """
    
    name: str
    # TODO: Store some info that could be used to preview the action?
    # prev_dict: Dict[Piece, Optional[Position]] = {}
    # TODO: Could also contain code to render this preview?
    #       With a lerp value?
    
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
    
    def realize(self, board):
        """
        Apply this outcome to the board state.
        """
        pass
    
    # TODO: This would be neat.
    def preview(self, surf, board, lerp: float):
        """
        Preview the action.
        """
        pass


class Move(Outcome):
    piece: object
    target: Position
    
    LERP_MAX: float = 0.5 # TODO: Make this a constant?
    
    def __init__(self, piece, target: Position):
        super().__init__()
        self.piece = piece
        self.target = target
    
    def realize(self, board):
        self.piece.move(self.target) # TODO: Go through board?
    
    def preview(self, surf, board, lerp: float):
        pass
    
class Capture(Move):
    captured: object
    
    def __init__(self, piece, target: Position, captured: object):
        super().__init__(piece, target)
        self.captured = captured
    
    def realize(self, board):
        super().realize(board)
        # board.remove_piece(self.captured)


class Promote(Move): # TODO: Could be capture???
    promoted_to: PieceType
    def __init__(self, piece, target: Position, promoted_to: PieceType = PieceType.QUEEN):
        super().__init__(piece, target)
        self.promoted_to = promoted_to
        
    def realize(self, board):
        super().realize(board)
        t = board.get_tile(self.target)
        print("REMOVED DUE TO CIRCULAR IMPORT ISSUE.")
        # new_piece = get_piece_class(self.promoted_to)(board, self.piece.loyalty, self.target)
        # t.piece = new_piece

class Castle(Outcome):
    king_piece: object
    rook_piece: object
    
    def __init__(self, king_piece, rook_piece):
        super().__init__()
        self.king_piece = king_piece
        self.rook_piece = rook_piece
    
    def realize(self, board):
        vec = self.rook_piece.position - self.king_piece.position
        vec = vec // abs(sum(vec)) # NOTE: Should work because it is a cardinal vector
        self.king_piece.move(self.king_piece.position + vec*2)
        self.rook_piece.move(self.king_piece.position - vec)

class Summon(Outcome):
    piece: object
    target: Position
    summoned: object
    
    def __init__(self, piece, target: Position, summoned: object):
        super().__init__()
        self.piece = piece
        self.target = target
        self.summoned = summoned
    
    def realize(self, board):
        super().realize(board)
        t, p = board.at_pos(self.target)
        if p is not None: # TODO: Debug, remove eventually.
            raise ValueError("CANNOT SUMMON: Board is occupied.")
        t.piece = self.summoned(loyalty=self.piece.loyalty, position=self.target)
