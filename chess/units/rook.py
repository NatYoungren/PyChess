import numpy as np

from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D
from chess.chess_types import Loyalty, Piece

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture


class RookCapture(Action):
    """
    Represents a move/capture action for a rook.
    """
    def update(self):
        super().update()
        
        for v in D.cardinal: # Cardinal vectors
            for pos, t, p in self.get_line(v, length=7, enemy_ok=True):
                self.outcomes[tuple(pos)] = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)


# TODO: Make enum?
class Rook(ChessPiece):
    def __init__(self, board, loyalty: Loyalty, position):
        # TODO: Sprite
        super().__init__(board=board, loyalty=loyalty, piece_type=Piece.ROOK, position=position)
        self.actions.append(RookCapture(self))
