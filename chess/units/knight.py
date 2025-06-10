import numpy as np
from typing import Tuple

from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D
from utils.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture


class KnightJump(Action):
    """
    Represents a move/capture action for a knight.
    """
    VECTORS: Tuple[Vector] = (D.f+D.f_l, D.f+D.f_r,
                              D.r+D.f_r, D.r+D.b_r,
                              D.b+D.b_l, D.b+D.b_r,
                              D.l+D.f_l, D.l+D.b_l)

    def update(self):
        super().update()
        for v in self.VECTORS: # Knight vectors
            pos, t, p = self.at_vec(v)
            if t is None: continue # OOB tile
            if t.is_blocked: continue # Blocked tile
            if t.is_void: continue # Void tile
            
            if p is None:
                self.add_outcome(t,  Move(self.piece, pos))
            elif p.loyalty != self.loyalty: # No friendly fire
                self.add_outcome(t, Capture(self.piece, pos, p))




class Knight(ChessPiece):
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.KNIGHT, position=position)    
        self.actions.append(KnightJump(self))
