import numpy as np

from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D
from utils.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture


class BishopCapture(Action):
    """
    Represents a move/capture action for a bishop.
    """
    def update(self):
        super().update()
        
        for v in D.diagonal: # Cardinal vectors
            for pos, t, p in self.get_line(v, length=7, enemy_ok=True):
                oc = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)
                self.add_outcome(t, oc)


class Bishop(ChessPiece):
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.BISHOP, position=position)
        self.actions.append(BishopCapture(self))
