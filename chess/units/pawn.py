import numpy as np
from typing import Tuple

from chess.chess_types import Position, Vector
from chess.chess_types import DirCls as D
from chess.chess_types import Loyalty, PieceType

from chess.units.piece import ChessPiece
from chess.actions.action import Action
from chess.actions.outcome import Move, Capture

class PawnMoveOnly(Action):
    """
    Represents a move action for a pawn.
    """
    def update(self):
        super().update()
        for pos, t, p in self.get_line(D.f,
                              length=2 if self.move_count == 0 else 1,
                              enemy_ok=False):
            self.outcomes[t] = Move(self.piece, pos)
        
class PawnCaptureOnly(Action):
    """
    Represents a capture action for a pawn.
    """
    def update(self):
        super().update()
        for v in (D.f_l, D.f_r):
            for pos, t, p in self.get_line(v,
                                          length=1,
                                          can_move=False):
                self.outcomes[t] = Capture(self.piece, pos, p)


class Pawn(ChessPiece):
    
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.PAWN, position=position)
        self.actions.append(PawnMoveOnly(self))
        self.actions.append(PawnCaptureOnly(self))
