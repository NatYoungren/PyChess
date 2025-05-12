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
    # TODO: Implement this!
    #       Have a helper for 'moves till blocked' with flag for capture or not.
    # OPTIONS_FIRST_TURN: Tuple[Vector] = (D.f, D.f*2)
    # OPTIONS: Tuple[Vector] = (D.f)
    def update(self):
        super().update()
        
        tdata = self.get_line(D.f,
                              length=2 if self.move_count == 0 else 1,
                              enemy_ok=False)
        for pos, t, p in tdata:
            self.outcomes[tuple(pos)] = Move(self.piece, pos)
        
class PawnCaptureOnly(Action):
    """
    Represents a capture action for a pawn.
    """
    CAPTURE_VECTORS: Tuple[Vector] = (D.f_l, D.f_r) # Left and right diagonal
    def update(self):
        super().update()
        
        for v in self.CAPTURE_VECTORS:
            pos, t, p = self.at_vec(v)
            if t is None: continue # OOB tile
            if p is None: continue # No piece to capture
            if p.loyalty == self.loyalty: continue # No friendly fire
            self.outcomes[tuple(pos)] = Capture(self.piece, pos, p)


class Pawn(ChessPiece):
    
    def __init__(self, loyalty: Loyalty, position):
        super().__init__(loyalty=loyalty, piece_type=PieceType.PAWN, position=position)
        self.actions.append(PawnMoveOnly(self))
        self.actions.append(PawnCaptureOnly(self))
