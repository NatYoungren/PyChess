import numpy as np

from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D
from chess.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture


class JesterDiagonal(Action):
    """
    Represents a diagonal move/capture action for a jester.
    """
    def update(self):
        super().update()
        if self.move_count % 2 == 1:
            return
        for v in D.diagonal: # Cardinal vectors
            for pos, t, p in self.get_line(v, length=7, enemy_ok=True):
                self.outcomes[t] = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)

class JesterCardinal(Action):
    """
    Represents a cardinal move/capture action for a jester.
    """
    def update(self):
        super().update()
        if self.move_count % 2 == 0:
            return
        for v in D.cardinal: # Cardinal vectors
            for pos, t, p in self.get_line(v, length=7, enemy_ok=True):
                self.outcomes[t] = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)

class Jester(ChessPiece):
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.JESTER, position=position)
        self.actions.append(JesterDiagonal(self))
        self.actions.append(JesterCardinal(self))
    
    @property
    def sprite(self):
        return self._sprite[self.move_count % 2]
