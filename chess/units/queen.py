import numpy as np

from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D
from utils.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture


class QueenCapture(Action):
    """
    Represents a move/capture action for a queen.
    """
    def update(self):
        super().update()
        
        for v in D.cardiagonal: # Cardinal vectors
            for pos, t, p in self.get_line(v, length=7, enemy_ok=True):
                self.add_outcome(t, Move(self.piece, pos) if p is None else Capture(self.piece, pos, p))



class Queen(ChessPiece):
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.QUEEN, position=position)
        self.actions.append(QueenCapture(self))