import numpy as np
from typing import Tuple

from utils.chess_types import Position, Vector
from utils.chess_types import DirCls as D
from utils.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture


class JesterDiagonal(Action):
    """
    Represents a diagonal move/capture action for a jester.
    """
    def update(self):
        super().update()
        if self.move_count % 2 == 0:
            return
        for v in D.diagonal: # Cardinal vectors
            for pos, t, p in self.get_line(v, length=2, enemy_ok=True): # NOTE: Testing limited length
                self.outcomes[t] = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)

# class JesterCardinal(Action):
#     """
#     Represents a cardinal move/capture action for a jester.
#     """
#     def update(self):
#         super().update()
#         if self.move_count % 2 == 0:
#             return
#         for v in D.cardinal: # Cardinal vectors
#             for pos, t, p in self.get_line(v, length=7, enemy_ok=True):
#                 self.outcomes[t] = Move(self.piece, pos) if p is None else Capture(self.piece, pos, p)

class JesterJump(Action):
    """
    Represents an L-shaped move/capture action for a jester.
    """
    VECTORS: Tuple[Vector] = (D.f+D.f_l, D.f+D.f_r)
    
    def update(self):
        super().update()
        if self.move_count % 2 == 1:
            return
        for d in D.cardinal: # Cardinal vectors
            for v in self.VECTORS: # Knight vectors
                pos, t, p = self.at_vec(self.orient_vector(v, d))
                if t is None: continue # OOB tile
                if t.is_blocked: continue # Blocked tile
                if t.is_void: continue # Void tile
                
                if p is None:
                    self.outcomes[t] = Move(self.piece, pos)
                elif p.loyalty != self.loyalty: # No friendly fire
                    self.outcomes[t] = Capture(self.piece, pos, p)




class Jester(ChessPiece):
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.JESTER, position=position)
        self.actions.append(JesterDiagonal(self))
        # self.actions.append(JesterCardinal(self))
        self.actions.append(JesterJump(self))
    
    @property
    def sprite(self):
        if isinstance(self._sprite, tuple):
            return self._sprite[(1+self.move_count) % 2]
        return self._sprite
